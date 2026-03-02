#!/bin/bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"

# Use venv protoc if available, otherwise system protoc
if [ -x "$REPO/.venv/bin/python" ]; then
  PROTOC="$REPO/.venv/bin/python -m grpc_tools.protoc"
  export PATH="$REPO/.venv/bin:$PATH"
else
  PROTOC="protoc"
fi

# Only regenerate _pb2.py runtime code.
# The .pyi type stubs are hand-written and maintained separately.
for svc in star resource liquid_handler; do
  for target in service client; do
    pkg="pylabrobot_protobuf_${target}"
    $PROTOC \
      --proto_path="$REPO/proto/$svc/v1" \
      --python_out="$REPO/src/$target/py/$pkg/$svc/_generated" \
      "$REPO/proto/$svc/v1/${svc}_service.proto"
  done
done
