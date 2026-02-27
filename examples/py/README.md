# Python Examples

## Prerequisites

Install the client package:

```bash
pip install pylabrobot-protobuf-client
```

## Running

Each example accepts a `--url` flag (or reads from environment variables) and defaults to `http://localhost:8080`.

### Aspirate

Connect to a STAR server and perform an aspirate operation:

```bash
python aspirate.py --url http://localhost:8080
```

### Channel Movement

Demonstrate channel movement on a STAR:

```bash
python move_channels.py --url http://localhost:8080
```

### Resource Query

Query a resource server and print the resource tree:

```bash
python resource_query.py --url http://localhost:8080
```
