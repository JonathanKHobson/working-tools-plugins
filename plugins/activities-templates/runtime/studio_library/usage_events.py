"""Optional metadata-only accounting at real MCP tool execution boundaries."""
import functools
import importlib.util
import inspect
import json
from pathlib import Path
import time
import uuid


def emit(operation, status, elapsed_ms):
    try:
        c=json.loads((Path.home()/'.config/studio-tools/usage-tracking.json').read_text())
        if c.get('enabled') is not True or not c.get('recorder_path'):return
        spec=importlib.util.spec_from_file_location('private_usage_ledger',c['recorder_path'])
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.record(dict(event_id=uuid.uuid4().hex,kind='plugin_server',plugin='activities-templates',
                           operation=operation,status=status,duration_ms=elapsed_ms))
    except Exception:
        pass


def tracked(fn, operation):
    if inspect.iscoroutinefunction(fn):
        @functools.wraps(fn)
        async def call(*args,**kwargs):
            started=time.monotonic();status='failure'
            try:
                value=await fn(*args,**kwargs)
                status='failure' if getattr(value,'isError',False) else 'success'
                return value
            finally:emit(operation,status,round((time.monotonic()-started)*1000))
    else:
        @functools.wraps(fn)
        def call(*args,**kwargs):
            started=time.monotonic();status='failure'
            try:
                value=fn(*args,**kwargs)
                status='failure' if getattr(value,'isError',False) else 'success'
                return value
            finally:emit(operation,status,round((time.monotonic()-started)*1000))
    return call


def install(server):
    original=server.tool
    def tool(*args,**kwargs):
        register=original(*args,**kwargs)
        def decorate(fn):
            register(tracked(fn,kwargs.get('name') or fn.__name__))
            return fn # Internal function reuse does not create a second tool event.
        return decorate
    server.tool=tool
