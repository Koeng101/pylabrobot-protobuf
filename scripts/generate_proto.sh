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

# Generate common types into every _generated/ dir
for svc in star resource liquid_handler; do
  for target in service client; do
    pkg="pylabrobot_protobuf_${target}"
    $PROTOC \
      --proto_path="$REPO/proto/common/v1" \
      --python_out="$REPO/src/$target/py/$pkg/$svc/_generated" \
      "$REPO/proto/common/v1/types.proto"
  done
done

# Generate service protos (with common proto_path for imports)
for svc in star resource liquid_handler; do
  for target in service client; do
    pkg="pylabrobot_protobuf_${target}"
    $PROTOC \
      --proto_path="$REPO/proto/$svc/v1" \
      --proto_path="$REPO/proto/common/v1" \
      --python_out="$REPO/src/$target/py/$pkg/$svc/_generated" \
      "$REPO/proto/$svc/v1/${svc}_service.proto"
  done
done

# Fix protoc absolute imports → relative imports for types_pb2.
# protoc generates `import types_pb2` which fails inside Python packages.
for svc in star resource liquid_handler; do
  for target in service client; do
    pkg="pylabrobot_protobuf_${target}"
    pb2="$REPO/src/$target/py/$pkg/$svc/_generated/${svc}_service_pb2.py"
    if [ -f "$pb2" ]; then
      sed -i 's/^import types_pb2 as/from . import types_pb2 as/' "$pb2"
    fi
  done
done
