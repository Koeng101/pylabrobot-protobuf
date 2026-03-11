# mypy: disable-error-code="method-assign,attr-defined,arg-type,index"
"""Basic liquid handling — the PLR 'hello world', but over the network.

## PLR (local, async)
#
#   lh = LiquidHandler(backend=STARBackend(), deck=deck)
#   await lh.setup()
#
#   await lh.pick_up_tips(lh.deck.get_resource("tip_rack")["A1"])
#   await lh.aspirate(lh.deck.get_resource("plate")["A1"], vols=100)
#   await lh.dispense(lh.deck.get_resource("plate")["A2"], vols=100)
#   await lh.return_tips()
#
## protobuf (remote, async)
#
#   lh = RemoteLiquidHandler.connect(lh_url)
#
#   await lh.pick_up_tips(["tip_rack_01_tipspot_A1"])
#   await lh.aspirate(["plate_01_well_A1"], vols=[100])
#   await lh.dispense(["plate_01_well_A2"], vols=[100])
#   await lh.return_tips()

Run:  python examples/py/basic.py
"""

import asyncio
import threading
import time
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
# Boilerplate: spin up mocked STAR + Resource + LH servers in-process
# ---------------------------------------------------------------------------

set_volume_tracking(False)
set_tip_tracking(False)

# Build deck
deck = STARLetDeck()
tip_car = TIP_CAR_480_A00(name="tip carrier")
tip_car[1] = hamilton_96_tiprack_300uL_filter(name="tip_rack_01")
deck.assign_child_resource(tip_car, rails=1)

plt_car = PLT_CAR_L5AC_A00(name="plate carrier")
plt_car[0] = Cor_96_wellplate_360ul_Fb(name="plate_01")
deck.assign_child_resource(plt_car, rails=9)

# Mock the STAR backend (no real hardware)
backend = STARBackend(read_timeout=1)
backend._write_and_read_command = unittest.mock.AsyncMock(return_value=None)
backend.io = unittest.mock.AsyncMock()
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
backend.set_deck(deck)

_STAR_PORT = 18_300
_RESOURCE_PORT = 18_301
_LH_PORT = 18_302

# Start STAR and Resource servers first (LH connects to them on creation)
servers = []
for app, port in [
  (create_star_app(backend), _STAR_PORT),
  (create_resource_app(deck), _RESOURCE_PORT),
]:
  srv = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error"))
  threading.Thread(target=srv.run, daemon=True).start()
  servers.append(srv)

time.sleep(1)  # wait for upstream servers to be ready

# Now start LH server (connects to STAR + Resource during init)
lh_app = create_liquid_handler_app(
  star_url=f"http://127.0.0.1:{_STAR_PORT}",
  resource_url=f"http://127.0.0.1:{_RESOURCE_PORT}",
)
srv = uvicorn.Server(uvicorn.Config(lh_app, host="127.0.0.1", port=_LH_PORT, log_level="error"))
threading.Thread(target=srv.run, daemon=True).start()
servers.append(srv)

time.sleep(0.5)
print("Servers ready.\n")

# ---------------------------------------------------------------------------
# The actual example — compare with the PLR snippet above
# ---------------------------------------------------------------------------


async def main():
  lh = RemoteLiquidHandler.connect(f"http://127.0.0.1:{_LH_PORT}")

  await lh.pick_up_tips(["tip_rack_01_tipspot_A1"])
  await lh.aspirate(["plate_01_well_A1"], vols=[100])
  await lh.dispense(["plate_01_well_A2"], vols=[100])
  await lh.return_tips()

  print("Done.")


asyncio.run(main())

# Shut down servers
for srv in servers:
  srv.should_exit = True
