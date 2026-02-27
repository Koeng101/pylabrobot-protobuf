# Multi-Language Client Generation

## Architecture

```
proto/                     buf generate         language-specific stubs
  star/v1/*.proto    ──────────────────────>    src/client/<lang>/
  deck/v1/*.proto                               examples/<lang>/
```

The Python server (`src/service/py/`) is the **reference implementation**. Clients in any language connect over [ConnectRPC](https://connectrpc.com/) (HTTP/1.1 + JSON or HTTP/2 + protobuf).

## Per-Language Generation

| Language | Client plugin | PLR adapter? | Output dir |
|----------|--------------|--------------|------------|
| Python | `connect-python` | Yes (`RemoteSTARBackend`, `RemoteDeck`) | `src/client/py/` |
| TypeScript | `@connectrpc/protoc-gen-connect-es` | No (raw stubs) | `src/client/ts/` |
| Go | `buf.build/connectrpc/go` | No | `src/client/go/` |
| Rust | `prost` + `tonic` | No | `src/client/rust/` |

### Python (current)

Python stubs are generated via `protoc` + `mypy-protobuf`. The ConnectRPC `_connect.py` files are currently hand-written because `connect-python` has no codegen plugin yet.

```bash
make proto
```

### TypeScript (planned)

```yaml
# buf.gen.yaml addition
plugins:
  - remote: buf.build/connectrpc/es
    out: ../src/client/ts/
    opt: target=ts
```

### Go (planned)

```yaml
# buf.gen.yaml addition
plugins:
  - remote: buf.build/connectrpc/go
    out: ../src/client/go/
    opt: paths=source_relative
```

### Rust (planned)

Rust generation uses `prost` + `tonic` via a `build.rs` script.

## Cross-Language Testing Strategy

### Test target

The Python server with mocked hardware serves as the test target for all languages.

### Shared test fixtures

A `testdata/` directory (planned) will contain JSON fixtures:

```json
{
  "rpc": "STARService/Setup",
  "request": {},
  "expected_response": {}
}
```

Each language reads these fixtures, calls the RPCs, and asserts the results match.

### CI pipeline

1. Start the mocked Python server
2. Run each language's client tests against it
3. Report per-language pass/fail

### Test levels

- **Conformance**: all RPC methods return expected responses
- **Error propagation**: server errors produce correct ConnectRPC error codes
- **Serialization fidelity**: complex nested messages round-trip correctly

## Phased Rollout

1. **Python** (current) — full server + client with PLR adapters
2. **TypeScript** — raw generated stubs + examples
3. **Go** — raw generated stubs + examples
4. **Rust** — raw generated stubs + examples

## Adding a New Language

1. Add a generation entry to `buf.gen.yaml`
2. Create `src/client/<lang>/` for generated stubs
3. Create `examples/<lang>/` with runnable examples
4. Add CI workflow for the new language's tests
5. Update this document
