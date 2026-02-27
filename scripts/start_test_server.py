#!/usr/bin/env python3
"""Start a mocked STARService for integration testing.

Prints "READY on port <N>" to stdout once the server is listening.
Shuts down cleanly on SIGTERM or SIGINT.
"""

from __future__ import annotations

import argparse
import signal
import sys
import threading
import time
import unittest.mock

import uvicorn
from pylabrobot.liquid_handling.backends.hamilton.STAR_backend import STARBackend
from pylabrobot.resources import (
  PLT_CAR_L5AC_A00,
  TIP_CAR_480_A00,
  Container,
  Coordinate,
  Cor_96_wellplate_360ul_Fb,
  Lid,
  hamilton_96_tiprack_300uL_filter,
  hamilton_96_tiprack_1000uL_filter,
)
from pylabrobot.resources.hamilton import STARLetDeck

from pylabrobot_protobuf_service.star import create_star_app

DEFAULT_PORT = 18770


def _init_backend_state(backend: STARBackend) -> None:
  backend._write_and_read_command = unittest.mock.AsyncMock(return_value=None)  # type: ignore[method-assign]
  backend.io = unittest.mock.AsyncMock()  # type: ignore[assignment]
  backend.io.setup = unittest.mock.AsyncMock()
  backend.io.write = unittest.mock.MagicMock()
  backend.io.read = unittest.mock.MagicMock()

  backend._num_channels = 8
  backend.iswap_installed = True
  backend.core96_head_installed = True
  backend._core_parked = True
  backend._iswap_parked = True

  backend._extended_conf = {
    "ka": 0, "ke": 0, "xt": 54, "xa": 30, "xw": 13130,
    "xl": 0, "xn": 0, "xr": 0, "xo": 0, "xm": 0,
    "xx": 0, "xu": 0, "xv": 0, "kc": 0, "kr": 0,
    "ys": 0, "kl": 0, "km": 0, "ym": 0, "yu": 0, "yx": 0,
  }
  backend.setup = unittest.mock.AsyncMock()  # type: ignore[method-assign]


class BlueBucket(Container):
  def __init__(self, name: str):
    super().__init__(
      name,
      size_x=123, size_y=82, size_z=75,
      category="bucket",
      max_volume=123 * 82 * 75,
      material_z_thickness=1,
    )


def _make_app() -> uvicorn.Config:
  backend = STARBackend(read_timeout=1)
  _init_backend_state(backend)

  deck = STARLetDeck()

  tip_car = TIP_CAR_480_A00(name="tip carrier")
  tip_car[1] = hamilton_96_tiprack_300uL_filter(name="tip_rack_01")
  tip_car[2] = hamilton_96_tiprack_1000uL_filter(name="tip_rack_02")
  deck.assign_child_resource(tip_car, rails=1)

  plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
  plate = Cor_96_wellplate_360ul_Fb(name="plate_01")
  lid = Lid(
    name="plate_01_lid",
    size_x=plate.get_size_x(),
    size_y=plate.get_size_y(),
    size_z=10,
    nesting_z_height=10,
  )
  plate.assign_child_resource(lid)
  plt_car[0] = plate
  deck.assign_child_resource(plt_car, rails=9)

  bb = BlueBucket(name="blue bucket")
  deck.assign_child_resource(bb, location=Coordinate(425, 141.5, 120 - 1))

  backend.set_deck(deck)
  return create_star_app(backend)


def main() -> None:
  parser = argparse.ArgumentParser(description="Start mocked STARService")
  parser.add_argument("--port", type=int, default=DEFAULT_PORT)
  args = parser.parse_args()

  app = _make_app()
  config = uvicorn.Config(app, host="127.0.0.1", port=args.port, log_level="error")
  server = uvicorn.Server(config)

  def _signal_handler(signum, frame):
    server.should_exit = True

  signal.signal(signal.SIGTERM, _signal_handler)
  signal.signal(signal.SIGINT, _signal_handler)

  # Start in a thread so we can print READY after startup.
  thread = threading.Thread(target=server.run, daemon=True)
  thread.start()
  time.sleep(0.8)

  print(f"READY on port {args.port}", flush=True)

  thread.join()


if __name__ == "__main__":
  main()
