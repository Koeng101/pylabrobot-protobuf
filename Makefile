.PHONY: test lint format format-check typecheck proto proto-check test-go

test:
	cd src/service/py && python -m pytest -s -v

lint:
	ruff check src/service/py src/client/py

format:
	ruff format src/service/py src/client/py
	ruff check --fix src/service/py src/client/py --select I

format-check:
	ruff format --check src/service/py src/client/py
	ruff check src/service/py src/client/py --select I

typecheck:
	cd src/service/py && mypy pylabrobot_protobuf_service
	cd src/client/py && mypy pylabrobot_protobuf_client

proto:
	bash scripts/generate_proto.sh
	cd proto && buf generate

test-go:
	cd src/client/go && go test -v -count=1 ./...

proto-check:
	bash scripts/generate_proto.sh
	git diff --exit-code -- 'src/**/*_pb2.py'
