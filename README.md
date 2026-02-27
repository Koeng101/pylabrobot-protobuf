# pylabrobot-protobuf

ConnectRPC service definitions and implementations for [PyLabRobot](https://github.com/PyLabRobot/pylabrobot).

## Services

- **STARService** (`proto/star/v1/`) — ~150 RPCs for Hamilton STAR liquid handler control
- **DeckService** (`proto/deck/v1/`) — 28 RPCs for deck resource management

## Packages

| Package | PyPI name | Description |
|---------|-----------|-------------|
| `src/service/py/` | `pylabrobot-protobuf-service` | Python server implementations |
| `src/client/py/` | `pylabrobot-protobuf-client` | Python client (PLR-compatible adapters) |

## Quick start

### Server

```bash
pip install pylabrobot-protobuf-service
```

```python
from pylabrobot_protobuf_service.star import create_star_app

app = create_star_app(backend)
# serve with uvicorn
```

### Client

```bash
pip install pylabrobot-protobuf-client
```

```python
from pylabrobot_protobuf_client.star import RemoteSTARBackend

remote = RemoteSTARBackend.connect("http://localhost:8080")
await remote.setup()
```

## Development

```bash
make format    # format code
make lint      # run linter
make typecheck # run mypy
make test      # run tests
make proto     # regenerate protobuf stubs
```

## Multi-language support

See [docs/MULTI_LANGUAGE_GENERATION.md](docs/MULTI_LANGUAGE_GENERATION.md) for generating client stubs in other languages.
