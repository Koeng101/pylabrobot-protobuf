"""Connect to a resource server, query the resource tree, and print the structure."""

from __future__ import annotations

import argparse
import os
import sys


def main(url: str) -> None:
  from pylabrobot_protobuf_client.resource import RemoteResource

  deck = RemoteResource.connect(url)
  print(f"Connected to resource server at {url}")
  print(f"Deck: {deck.name} ({deck.get_size_x():.0f} x {deck.get_size_y():.0f} x "
        f"{deck.get_size_z():.0f})")
  print()

  def print_tree(resource, indent: int = 0) -> None:
    prefix = "  " * indent
    loc = resource.location
    loc_str = f"({loc.x:.1f}, {loc.y:.1f}, {loc.z:.1f})" if loc else "(no location)"
    print(f"{prefix}{resource.name} [{type(resource).__name__}] at {loc_str}")
    for child in resource.children:
      print_tree(child, indent + 1)

  for child in deck.children:
    print_tree(child)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Resource structure query example")
  parser.add_argument(
    "--url",
    default=os.environ.get("RESOURCE_URL", "http://localhost:8080"),
    help="Resource server URL (default: http://localhost:8080)",
  )
  args = parser.parse_args()

  try:
    main(args.url)
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
