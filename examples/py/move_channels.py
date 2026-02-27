"""Connect to a STAR server and demonstrate channel movement."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys


async def main(url: str) -> None:
  from pylabrobot_protobuf_client.star import RemoteSTARBackend

  remote = RemoteSTARBackend.connect(url)
  print(f"Connected to STAR server at {url}")

  await remote.setup()
  print("Setup complete")

  num_channels = remote.num_channels
  print(f"Available channels: {num_channels}")

  await remote.stop()
  print("Done")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="STAR channel movement example")
  parser.add_argument(
    "--url",
    default=os.environ.get("STAR_URL", "http://localhost:8080"),
    help="STAR server URL (default: http://localhost:8080)",
  )
  args = parser.parse_args()

  try:
    asyncio.run(main(args.url))
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
