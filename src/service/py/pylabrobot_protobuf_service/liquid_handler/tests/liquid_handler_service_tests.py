# mypy: disable-error-code="method-assign,attr-defined,arg-type,index"
"""Integration tests for the LiquidHandler service.

Spins up all three services (STAR, Resource, LiquidHandler) and exercises
the full lifecycle through the RemoteLiquidHandler client.
"""

import asyncio
import threading
import time
import unittest
import unittest.mock

import uvicorn
from pylabrobot.liquid_handling.backends.hamilton.STAR_backend import STARBackend
from pylabrobot.resources import (
  PLT_CAR_L5AC_A00,
  TIP_CAR_480_A00,
  Cor_96_wellplate_360ul_Fb,
  hamilton_96_tiprack_300uL_filter,
)
from pylabrobot.resources.hamilton import STARLetDeck
from pylabrobot.resources.tip_tracker import set_tip_tracking
from pylabrobot.resources.volume_tracker import set_volume_tracking

from pylabrobot_protobuf_client.liquid_handler import RemoteLiquidHandler
from pylabrobot_protobuf_service.liquid_handler import create_liquid_handler_app
from pylabrobot_protobuf_service.resource.server import create_app as create_resource_app
from pylabrobot_protobuf_service.star import create_star_app

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _init_backend_state(backend: STARBackend) -> None:
  """Mock the backend hardware layer to avoid serial communication."""
  backend._write_and_read_command = unittest.mock.AsyncMock(return_value=None)
  backend.io = unittest.mock.AsyncMock()
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
  backend.setup = unittest.mock.AsyncMock()


class _ServerFixture:
  """Spin up a uvicorn server in a background thread and tear it down after."""

  def __init__(self, app, port: int):
    self.port = port
    self._app = app
    self._server: uvicorn.Server | None = None
    self._thread: threading.Thread | None = None

  def start(self):
    config = uvicorn.Config(self._app, host="127.0.0.1", port=self.port, log_level="error")
    self._server = uvicorn.Server(config)
    self._thread = threading.Thread(target=self._server.run, daemon=True)
    self._thread.start()
    time.sleep(0.8)

  def stop(self):
    if self._server is not None:
      self._server.should_exit = True
    if self._thread is not None:
      self._thread.join(timeout=3)

  @property
  def url(self) -> str:
    return f"http://127.0.0.1:{self.port}"


def _make_deck() -> STARLetDeck:
  """Build a deck with a tip rack and a plate for testing."""
  deck = STARLetDeck()

  tip_car = TIP_CAR_480_A00(name="tip carrier")
  tip_car[1] = hamilton_96_tiprack_300uL_filter(name="tip_rack_01")
  deck.assign_child_resource(tip_car, rails=1)

  plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
  plate = Cor_96_wellplate_360ul_Fb(name="plate_01")
  plt_car[0] = plate
  deck.assign_child_resource(plt_car, rails=9)

  return deck


# ---------------------------------------------------------------------------
# Port allocation
# ---------------------------------------------------------------------------

_STAR_PORT = 18_200
_RESOURCE_PORT = 18_201
_LH_PORT = 18_202


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


class TestLiquidHandlerIntegration(unittest.TestCase):
  """Full integration: Client → LH Service → STAR + Resource services."""

  @classmethod
  def setUpClass(cls):
    set_volume_tracking(False)
    set_tip_tracking(False)

    deck = _make_deck()
    backend = STARBackend(read_timeout=1)
    _init_backend_state(backend)
    backend.set_deck(deck)

    cls.star_fixture = _ServerFixture(create_star_app(backend), _STAR_PORT)
    cls.resource_fixture = _ServerFixture(create_resource_app(deck), _RESOURCE_PORT)
    cls.lh_fixture = _ServerFixture(
      create_liquid_handler_app(
        star_url=f"http://127.0.0.1:{_STAR_PORT}",
        resource_url=f"http://127.0.0.1:{_RESOURCE_PORT}",
      ),
      _LH_PORT,
    )

    cls.star_fixture.start()
    cls.resource_fixture.start()
    cls.lh_fixture.start()

    cls.client = RemoteLiquidHandler.connect(cls.lh_fixture.url)
    asyncio.run(cls.client.setup())

  @classmethod
  def tearDownClass(cls):
    try:
      asyncio.run(cls.client.stop())
    except Exception:
      pass
    cls.lh_fixture.stop()
    cls.resource_fixture.stop()
    cls.star_fixture.stop()

  # -- tip operations --

  def test_pick_up_and_drop_tips(self):
    asyncio.run(self.client.pick_up_tips(["tip_rack_01_tipspot_A1"]))
    asyncio.run(self.client.drop_tips(["tip_rack_01_tipspot_A1"]))

  # -- liquid operations --

  def test_aspirate_and_dispense(self):
    asyncio.run(self.client.pick_up_tips(["tip_rack_01_tipspot_B1"]))
    asyncio.run(self.client.aspirate(["plate_01_well_A1"], vols=[50.0]))
    asyncio.run(self.client.dispense(["plate_01_well_A2"], vols=[50.0]))
    asyncio.run(self.client.drop_tips(["tip_rack_01_tipspot_B1"]))

  # -- state queries --

  def test_get_mounted_tips(self):
    tips = asyncio.run(self.client.get_mounted_tips())
    self.assertEqual(len(tips), 8)

  def test_get_picked_up_resource_none(self):
    resource = asyncio.run(self.client.get_picked_up_resource())
    self.assertIsNone(resource)


if __name__ == "__main__":
  unittest.main()
