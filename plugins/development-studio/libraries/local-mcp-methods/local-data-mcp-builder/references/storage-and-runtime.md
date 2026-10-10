# Storage and Runtime

## Placement defaults

- Put large indexes, raw data, and temp build artifacts on the larger SSD.
- Put the runtime in a stable path, especially if the external drive has filesystem quirks.

## Why separate them

Large MCPs often create:

- SQLite DB files
- large WAL files during index builds
- chunk caches
- extracted metadata

Those belong on the roomy disk.

The runtime is different:

- Python virtualenvs are sensitive to broken metadata files
- they are small compared with the indexed data
- keeping them in a stable home-directory path can be more reliable

## External-drive AppleDouble issue

On some macOS hosts, a virtualenv created on `<external-ssd>` picked up `._*` AppleDouble files such as:

- `._distutils-precedence.pth`

Those files caused Python startup failures. The fix was:

1. keep the MCP data and SQLite DB on the external SSD
2. move the Python runtime to a home-directory location
3. clean stray `._*` files if needed

## Practical rule

If the external drive is roomy but Python gets weird, move only the runtime. Do not move the large indexed data unless storage requires it.

## Claude Desktop launch rule

Even when the runtime is healthy, Claude Desktop on some macOS hosts has rejected shell wrapper scripts on `<external-volume>` with `Operation not permitted`.

Preferred Claude Desktop launch shape:

- `command`: home-directory interpreter path
- `args`: external-drive server script path plus data flags

Avoid:

- `command = /bin/bash`
- `args = [<external-volume>/run_server.sh]`
