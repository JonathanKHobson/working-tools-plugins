"""Private fixed-service SDK backend, started on demand and retired after idle."""
from __future__ import annotations

import argparse
import fcntl
from functools import partial, wraps
import inspect
import json
import os
from pathlib import Path
import stat
import time

import anyio
from anyio.abc import SocketAttribute
from mcp.server.fastmcp import FastMCP
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCError, JSONRPCMessage, JSONRPCRequest, JSONRPCResponse

from stdio_proxy import CHUNK, locked_file, peer_uid

MAX_LINE = 16 * 1024 * 1024


def threaded(fn):
    if inspect.iscoroutinefunction(fn):
        return fn

    @wraps(fn)
    async def call(*args, **kwargs):
        # Do not abandon an executing feedback write on client disconnect.
        result = await anyio.to_thread.run_sync(partial(fn, *args, **kwargs))
        # Once the write is complete, deliver any pending cancellation to the SDK
        # before it attempts a second response to an already cancelled request.
        await anyio.lowlevel.checkpoint()
        return result
    return call


class ThreadedFastMCP(FastMCP):
    """Keep SDK schemas/validation while blocking catalog work runs off the loop."""
    def tool(self, *args, **kwargs):
        register = super().tool(*args, **kwargs)

        def decorate(fn):
            register(threaded(fn))
            return fn
        return decorate

    def resource(self, *args, **kwargs):
        register = super().resource(*args, **kwargs)

        def decorate(fn):
            register(threaded(fn))
            return fn
        return decorate


async def read_line(stream, pending, limit):
    while True:
        split = pending.find(b'\n')
        if split >= 0:
            if split > limit:
                raise ValueError('Incoming transport line exceeds limit')
            line = bytes(pending[:split + 1])
            del pending[:split + 1]
            return line
        if len(pending) > limit:
            raise ValueError('Incoming transport line exceeds limit')
        try:
            pending.extend(await stream.receive(min(CHUNK, limit + 1 - len(pending))))
        except anyio.EndOfStream:
            line = bytes(pending)
            pending.clear()
            return line


async def sdk_transport(stream, pending, server, *, eof_drain_seconds=30):
    """Mirror SDK stdio parsing and zero-capacity streams, retaining session semantics."""
    read_writer, read_stream = anyio.create_memory_object_stream(0)
    write_stream, write_reader = anyio.create_memory_object_stream(0)
    writer_done = anyio.Event()
    pending_requests = set()
    drained = anyio.Event()
    drained.set()

    async def reader():
        nonlocal drained
        async with read_writer:
            while True:
                line = await read_line(stream, pending, MAX_LINE)
                if not line:
                    # SDK's receive loop closes its output handle on input EOF.
                    # Keep that handle open until accepted requests have replied.
                    if pending_requests:
                        # A dropped SDK response must not retain this connection
                        # forever. Executing shielded handlers still finish in run().
                        with anyio.move_on_after(eof_drain_seconds):
                            await drained.wait()
                    return
                try:
                    message = SessionMessage(JSONRPCMessage.model_validate_json(line))
                    if isinstance(message.message.root, JSONRPCRequest):
                        if not pending_requests:
                            drained = anyio.Event()
                        pending_requests.add(message.message.root.id)
                except Exception as exc:
                    message = exc
                await read_writer.send(message)

    async def writer():
        try:
            async with write_reader:
                async for message in write_reader:
                    data = message.message.model_dump_json(by_alias=True, exclude_none=True).encode() + b'\n'
                    for start in range(0, len(data), CHUNK):
                        await stream.send(data[start:start + CHUNK])
                    if isinstance(message.message.root, (JSONRPCResponse, JSONRPCError)):
                        pending_requests.discard(message.message.root.id)
                        if not pending_requests:
                            drained.set()
        finally:
            writer_done.set()

    async with anyio.create_task_group() as group:
        group.start_soon(reader)
        group.start_soon(writer)
        try:
            await server._mcp_server.run(read_stream, write_stream,
                                         server._mcp_server.create_initialization_options())
        finally:
            await write_stream.aclose()
            await read_stream.aclose()
        await writer_done.wait()
        group.cancel_scope.cancel()


async def serve(args):
    from server import create_server
    clients = 0
    last_empty = time.monotonic()
    idle_seconds = max(0.1, float(os.environ.get('BRAND_BACKEND_IDLE_SECONDS', '60')))
    # bind() creates the filesystem socket before AnyIO's explicit chmod. Establish
    # the private mode at creation so a simultaneous proxy never observes 0755.
    previous_umask = os.umask(0o177)
    try:
        listener = await anyio.create_unix_listener(args.socket, mode=0o600)
    finally:
        os.umask(previous_umask)
    receipt = args.socket.with_suffix('.pid')
    receipt_fd = locked_file(receipt)
    try:
        os.ftruncate(receipt_fd, 0)
        os.write(receipt_fd, json.dumps({'pid': os.getpid(), 'service': 'brand-library',
                                       'key': args.key, 'socket': str(args.socket)}).encode())
    finally:
        os.close(receipt_fd)

    async def client(stream):
        nonlocal clients, last_empty
        # Count accepted connections, including waiting handshakes, before first await.
        clients += 1
        try:
            async with stream:
                if peer_uid(stream.extra(SocketAttribute.raw_socket)) != os.getuid():
                    return
                pending = bytearray()
                with anyio.fail_after(20):
                    greeting = json.loads(await read_line(stream, pending, 1024))
                    if greeting != {'key': args.key, 'service': 'brand-library'}:
                        await stream.send(b'{"error":"Backend service binding mismatch"}\n')
                        return
                    try:
                        server = await anyio.to_thread.run_sync(
                            lambda: create_server(server_class=ThreadedFastMCP))
                    except Exception as exc:
                        await stream.send(json.dumps({'error': 'Backend catalog unavailable: ' + type(exc).__name__}).encode() + b'\n')
                        return
                    await stream.send(b'{"ready":true}\n')
                await sdk_transport(stream, pending, server)
        except Exception:
            # A malformed line/disconnected peer affects only this SDK session. Tool
            # exceptions and protocol errors are already handled by the MCP SDK.
            pass
        finally:
            clients -= 1
            if not clients:
                last_empty = time.monotonic()

    async def retire(group):
        while True:
            await anyio.sleep(min(idle_seconds, 1))
            if not clients and time.monotonic() - last_empty >= idle_seconds:
                # No await between the idle decision and cancellation of accepts.
                group.cancel_scope.cancel()
                return

    try:
        async with listener, anyio.create_task_group() as group:
            group.start_soon(retire, group)
            await listener.serve(client)
    finally:
        args.socket.unlink(missing_ok=True)
        receipt.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--socket', type=Path, required=True)
    parser.add_argument('--key', required=True)
    args = parser.parse_args()
    directory = args.socket.parent.lstat()
    if not stat.S_ISDIR(directory.st_mode) or directory.st_uid != os.getuid() or stat.S_IMODE(directory.st_mode) != 0o700:
        raise ValueError('Unsafe backend socket directory')
    fd = locked_file(args.socket.with_suffix('.lease'))
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        # A lifetime lease proves that any old socket is stale before removing it.
        if args.socket.exists() or args.socket.is_symlink():
            old = args.socket.lstat()
            if not stat.S_ISSOCK(old.st_mode) or old.st_uid != os.getuid():
                raise ValueError('Unsafe backend socket')
            args.socket.unlink()
        anyio.run(serve, args)
    finally:
        os.close(fd)


if __name__ == '__main__':
    main()
