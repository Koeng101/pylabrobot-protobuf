"""LiquidHandlerService server implementation — coordinator wrapping LiquidHandler."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Optional, Union, cast

from connectrpc.code import Code
from connectrpc.errors import ConnectError
from pylabrobot.liquid_handling.liquid_handler import GripDirection, LiquidHandler
from pylabrobot.resources.container import Container
from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.plate import Lid, Plate
from pylabrobot.resources.resource import Resource
from pylabrobot.resources.tip_rack import TipRack, TipSpot
from pylabrobot.resources.trash import Trash

from pylabrobot_protobuf_client.resource import RemoteResource
from pylabrobot_protobuf_client.star import RemoteSTARBackend

from ._generated import liquid_handler_service_pb2 as pb2
from ._generated import types_pb2
from ._generated.liquid_handler_service_connect import (
  LiquidHandlerService,
  LiquidHandlerServiceASGIApplication,
)

if TYPE_CHECKING:
  from connectrpc.request import RequestContext


# ============================================================
# Conversion helpers
# ============================================================

_GRIP_DIR_MAP: dict[int, GripDirection] = {
  int(pb2.GRIP_DIRECTION_FRONT): GripDirection.FRONT,
  int(pb2.GRIP_DIRECTION_BACK): GripDirection.BACK,
  int(pb2.GRIP_DIRECTION_LEFT): GripDirection.LEFT,
  int(pb2.GRIP_DIRECTION_RIGHT): GripDirection.RIGHT,
}


def _to_grip_direction(proto_dir: int) -> GripDirection:
  return _GRIP_DIR_MAP.get(proto_dir, GripDirection.FRONT)


def _to_coord(c: types_pb2.Coordinate) -> Coordinate:
  return Coordinate(x=c.x, y=c.y, z=c.z)


def _optional_float(f: pb2.OptionalFloat) -> Optional[float]:
  """Extract value from OptionalFloat, returning None if not set."""
  return f.value if f.HasField("value") else None


def _optional_floats(fs: list[pb2.OptionalFloat]) -> Optional[list[Optional[float]]]:
  """Convert repeated OptionalFloat to list of Optional[float], or None if empty."""
  if not fs:
    return None
  return [_optional_float(f) for f in fs]


def _resolve_destination(
  deck: Resource,
  request: object,
) -> Union[Resource, Coordinate]:
  """Resolve a oneof destination field to a Resource or Coordinate."""
  dest = getattr(request, "WhichOneof", lambda _: None)("destination")
  if dest == "to_name":
    return deck.get_resource(getattr(request, "to_name"))
  if dest == "to_coordinate":
    return _to_coord(getattr(request, "to_coordinate"))
  raise ConnectError(Code.INVALID_ARGUMENT, "destination is required")


# ============================================================
# Service implementation
# ============================================================


class LiquidHandlerServiceImpl(LiquidHandlerService):
  """ConnectRPC service that wraps a LiquidHandler connected to remote STAR and Resource servers."""

  def __init__(self, star_url: str, resource_url: str) -> None:
    backend = RemoteSTARBackend.connect(star_url)
    deck = RemoteResource.connect(resource_url)
    self._lh = LiquidHandler(backend=backend, deck=deck)

  # --- Single-channel tips ---

  async def pick_up_tips(self, request: pb2.PickUpTipsRequest, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    tip_spots = [cast(TipSpot, lh.deck.get_resource(n)) for n in request.tip_spot_names]
    use_channels = list(request.use_channels) if request.use_channels else None
    offsets = [_to_coord(o) for o in request.offsets] if request.offsets else None
    await lh.pick_up_tips(tip_spots=tip_spots, use_channels=use_channels, offsets=offsets)
    return types_pb2.Empty()

  async def drop_tips(self, request: pb2.DropTipsRequest, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    tip_spots: list[Union[TipSpot, Trash]] = [
      cast(Union[TipSpot, Trash], lh.deck.get_resource(n)) for n in request.tip_spot_names
    ]
    use_channels = list(request.use_channels) if request.use_channels else None
    offsets = [_to_coord(o) for o in request.offsets] if request.offsets else None
    await lh.drop_tips(
      tip_spots=tip_spots,
      use_channels=use_channels,
      offsets=offsets,
      allow_nonzero_volume=request.allow_nonzero_volume,
    )
    return types_pb2.Empty()

  async def return_tips(self, request: pb2.ReturnTipsRequest, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    use_channels = list(request.use_channels) if request.use_channels else None
    offsets = [_to_coord(o) for o in request.offsets] if request.offsets else None
    await lh.return_tips(
      use_channels=use_channels,
      allow_nonzero_volume=request.allow_nonzero_volume,
      offsets=offsets,
    )
    return types_pb2.Empty()

  async def discard_tips(self, request: pb2.DiscardTipsRequest, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    use_channels = list(request.use_channels) if request.use_channels else None
    offsets = [_to_coord(o) for o in request.offsets] if request.offsets else None
    await lh.discard_tips(
      use_channels=use_channels,
      allow_nonzero_volume=request.allow_nonzero_volume,
      offsets=offsets,
    )
    return types_pb2.Empty()

  # --- Single-channel liquid ---

  async def aspirate(self, request: pb2.AspirateRequest, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    resources = [cast(Container, lh.deck.get_resource(n)) for n in request.resource_names]
    vols = list(request.vols)
    use_channels = list(request.use_channels) if request.use_channels else None
    offsets = [_to_coord(o) for o in request.offsets] if request.offsets else None
    await lh.aspirate(
      resources,
      vols,
      use_channels=use_channels,
      flow_rates=_optional_floats(list(request.flow_rates)),
      offsets=offsets,
      liquid_height=_optional_floats(list(request.liquid_height)),
      blow_out_air_volume=_optional_floats(list(request.blow_out_air_volume)),
    )
    return types_pb2.Empty()

  async def dispense(self, request: pb2.DispenseRequest, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    resources = [cast(Container, lh.deck.get_resource(n)) for n in request.resource_names]
    vols = list(request.vols)
    use_channels = list(request.use_channels) if request.use_channels else None
    offsets = [_to_coord(o) for o in request.offsets] if request.offsets else None
    await lh.dispense(
      resources,
      vols,
      use_channels=use_channels,
      flow_rates=_optional_floats(list(request.flow_rates)),
      offsets=offsets,
      liquid_height=_optional_floats(list(request.liquid_height)),
      blow_out_air_volume=_optional_floats(list(request.blow_out_air_volume)),
    )
    return types_pb2.Empty()

  # --- 96-head tips ---

  async def pick_up_tips96(
    self, request: pb2.PickUpTips96Request, ctx: RequestContext
  ) -> types_pb2.Empty:
    lh = self._lh
    tip_rack = cast(TipRack, lh.deck.get_resource(request.tip_rack_name))
    offset = _to_coord(request.offset) if request.HasField("offset") else Coordinate.zero()
    await lh.pick_up_tips96(tip_rack=tip_rack, offset=offset)
    return types_pb2.Empty()

  async def drop_tips96(self, request: pb2.DropTips96Request, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    resource = cast(Union[TipRack, Trash], lh.deck.get_resource(request.resource_name))
    offset = _to_coord(request.offset) if request.HasField("offset") else Coordinate.zero()
    await lh.drop_tips96(
      resource=resource,
      offset=offset,
      allow_nonzero_volume=request.allow_nonzero_volume,
    )
    return types_pb2.Empty()

  async def return_tips96(
    self, request: pb2.ReturnTips96Request, ctx: RequestContext
  ) -> types_pb2.Empty:
    lh = self._lh
    offset = _to_coord(request.offset) if request.HasField("offset") else Coordinate.zero()
    await lh.return_tips96(
      allow_nonzero_volume=request.allow_nonzero_volume,
      offset=offset,
    )
    return types_pb2.Empty()

  async def discard_tips96(
    self, request: pb2.DiscardTips96Request, ctx: RequestContext
  ) -> types_pb2.Empty:
    lh = self._lh
    await lh.discard_tips96(allow_nonzero_volume=request.allow_nonzero_volume)
    return types_pb2.Empty()

  # --- 96-head liquid ---

  async def aspirate96(self, request: pb2.Aspirate96Request, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    resource = lh.deck.get_resource(request.resource_name)
    offset = _to_coord(request.offset) if request.HasField("offset") else Coordinate.zero()
    flow_rate = _optional_float(request.flow_rate) if request.HasField("flow_rate") else None
    liquid_height = (
      _optional_float(request.liquid_height) if request.HasField("liquid_height") else None
    )
    blow_out = (
      _optional_float(request.blow_out_air_volume)
      if request.HasField("blow_out_air_volume")
      else None
    )
    await lh.aspirate96(
      resource=resource,
      volume=request.volume,
      offset=offset,
      flow_rate=flow_rate,
      liquid_height=liquid_height,
      blow_out_air_volume=blow_out,
    )
    return types_pb2.Empty()

  async def dispense96(self, request: pb2.Dispense96Request, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    resource = lh.deck.get_resource(request.resource_name)
    offset = _to_coord(request.offset) if request.HasField("offset") else Coordinate.zero()
    flow_rate = _optional_float(request.flow_rate) if request.HasField("flow_rate") else None
    liquid_height = (
      _optional_float(request.liquid_height) if request.HasField("liquid_height") else None
    )
    blow_out = (
      _optional_float(request.blow_out_air_volume)
      if request.HasField("blow_out_air_volume")
      else None
    )
    await lh.dispense96(
      resource=resource,
      volume=request.volume,
      offset=offset,
      flow_rate=flow_rate,
      liquid_height=liquid_height,
      blow_out_air_volume=blow_out,
    )
    return types_pb2.Empty()

  # --- Resource movement (high-level) ---

  async def move_resource(
    self, request: pb2.MoveResourceRequest, ctx: RequestContext
  ) -> types_pb2.Empty:
    lh = self._lh
    resource = lh.deck.get_resource(request.resource_name)
    to = _resolve_destination(lh.deck, request)
    intermediate = (
      [_to_coord(c) for c in request.intermediate_locations]
      if request.intermediate_locations
      else None
    )
    pickup_offset = (
      _to_coord(request.pickup_offset) if request.HasField("pickup_offset") else Coordinate.zero()
    )
    dest_offset = (
      _to_coord(request.destination_offset)
      if request.HasField("destination_offset")
      else Coordinate.zero()
    )
    await lh.move_resource(
      resource=resource,
      to=to,
      intermediate_locations=intermediate,
      pickup_offset=pickup_offset,
      destination_offset=dest_offset,
      pickup_distance_from_top=request.pickup_distance_from_top,
      pickup_direction=_to_grip_direction(request.pickup_direction),
      drop_direction=_to_grip_direction(request.drop_direction),
    )
    return types_pb2.Empty()

  async def move_plate(self, request: pb2.MovePlateRequest, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    plate = cast(Plate, lh.deck.get_resource(request.plate_name))
    to = _resolve_destination(lh.deck, request)
    intermediate = (
      [_to_coord(c) for c in request.intermediate_locations]
      if request.intermediate_locations
      else None
    )
    pickup_offset = (
      _to_coord(request.pickup_offset) if request.HasField("pickup_offset") else Coordinate.zero()
    )
    dest_offset = (
      _to_coord(request.destination_offset)
      if request.HasField("destination_offset")
      else Coordinate.zero()
    )
    kwargs: dict = dict(
      plate=plate,
      to=to,
      intermediate_locations=intermediate,
      pickup_offset=pickup_offset,
      destination_offset=dest_offset,
      pickup_direction=_to_grip_direction(request.pickup_direction),
      drop_direction=_to_grip_direction(request.drop_direction),
    )
    if request.HasField("pickup_distance_from_top"):
      dist = _optional_float(request.pickup_distance_from_top)
      if dist is not None:
        kwargs["pickup_distance_from_top"] = dist
    await lh.move_plate(**kwargs)
    return types_pb2.Empty()

  async def move_lid(self, request: pb2.MoveLidRequest, ctx: RequestContext) -> types_pb2.Empty:
    lh = self._lh
    lid = cast(Lid, lh.deck.get_resource(request.lid_name))
    to = _resolve_destination(lh.deck, request)
    intermediate = (
      [_to_coord(c) for c in request.intermediate_locations]
      if request.intermediate_locations
      else None
    )
    pickup_offset = (
      _to_coord(request.pickup_offset) if request.HasField("pickup_offset") else Coordinate.zero()
    )
    dest_offset = (
      _to_coord(request.destination_offset)
      if request.HasField("destination_offset")
      else Coordinate.zero()
    )
    kwargs: dict = dict(
      lid=lid,
      to=to,
      intermediate_locations=intermediate,
      pickup_offset=pickup_offset,
      destination_offset=dest_offset,
      pickup_direction=_to_grip_direction(request.pickup_direction),
      drop_direction=_to_grip_direction(request.drop_direction),
    )
    if request.HasField("pickup_distance_from_top"):
      dist = _optional_float(request.pickup_distance_from_top)
      if dist is not None:
        kwargs["pickup_distance_from_top"] = dist
    await lh.move_lid(**kwargs)
    return types_pb2.Empty()

  # --- Resource movement (low-level 3-step) ---

  async def pick_up_resource(
    self, request: pb2.PickUpResourceRequest, ctx: RequestContext
  ) -> types_pb2.Empty:
    lh = self._lh
    resource = lh.deck.get_resource(request.resource_name)
    offset = _to_coord(request.offset) if request.HasField("offset") else Coordinate.zero()
    pickup_dist = (
      _optional_float(request.pickup_distance_from_top)
      if request.HasField("pickup_distance_from_top")
      else None
    )
    await lh.pick_up_resource(
      resource=resource,
      offset=offset,
      pickup_distance_from_top=pickup_dist,
      direction=_to_grip_direction(request.direction),
    )
    return types_pb2.Empty()

  async def move_picked_up_resource(
    self, request: pb2.MovePickedUpResourceRequest, ctx: RequestContext
  ) -> types_pb2.Empty:
    lh = self._lh
    to = _to_coord(request.to)
    offset = _to_coord(request.offset) if request.HasField("offset") else Coordinate.zero()
    direction = (
      _to_grip_direction(request.direction) if request.HasField("direction") else None
    )
    await lh.move_picked_up_resource(to=to, offset=offset, direction=direction)
    return types_pb2.Empty()

  async def drop_resource(
    self, request: pb2.DropResourceRequest, ctx: RequestContext
  ) -> types_pb2.Empty:
    lh = self._lh
    dest_field = request.WhichOneof("destination")
    destination: Union[Resource, Coordinate]
    if dest_field == "destination_name":
      destination = lh.deck.get_resource(request.destination_name)
    elif dest_field == "destination_coordinate":
      destination = _to_coord(request.destination_coordinate)
    else:
      raise ConnectError(Code.INVALID_ARGUMENT, "destination is required")
    offset = _to_coord(request.offset) if request.HasField("offset") else Coordinate.zero()
    await lh.drop_resource(
      destination=destination,
      offset=offset,
      direction=_to_grip_direction(request.direction),
    )
    return types_pb2.Empty()

  # --- State queries ---

  async def get_mounted_tips(
    self, request: types_pb2.Empty, ctx: RequestContext
  ) -> pb2.GetMountedTipsResponse:
    lh = self._lh
    tips = lh.get_mounted_tips()
    tip_infos = []
    for i, tip in enumerate(tips):
      info = pb2.TipInfo(channel=i, has_tip=tip is not None)
      if tip is not None:
        info.total_tip_length = tip.total_tip_length
        info.maximal_volume = tip.maximal_volume
        info.has_filter = tip.has_filter
        info.fitting_depth = tip.fitting_depth
      tip_infos.append(info)
    return pb2.GetMountedTipsResponse(tips=tip_infos)

  async def get_picked_up_resource(
    self, request: types_pb2.Empty, ctx: RequestContext
  ) -> pb2.GetPickedUpResourceResponse:
    lh = self._lh
    resource = lh.get_picked_up_resource()
    if resource is not None:
      return pb2.GetPickedUpResourceResponse(has_resource=True, resource_name=resource.name)
    return pb2.GetPickedUpResourceResponse(has_resource=False)


# ============================================================
# ASGI app factory
# ============================================================


def create_liquid_handler_app(
  star_url: str,
  resource_url: str,
) -> Any:
  """Create an ASGI application for the LiquidHandler coordinator service.

  The returned app calls ``LiquidHandler.setup()`` on ASGI startup and
  ``LiquidHandler.stop()`` on shutdown via the ASGI lifespan protocol.

  Args:
    star_url: URL of the STAR backend ConnectRPC service.
    resource_url: URL of the Resource/Deck ConnectRPC service.

  Usage::

      import uvicorn
      from pylabrobot_protobuf_service.liquid_handler import create_liquid_handler_app

      app = create_liquid_handler_app(
        star_url="http://localhost:8080",
        resource_url="http://localhost:8081",
      )
      uvicorn.run(app, host="0.0.0.0", port=8082)
  """
  svc = LiquidHandlerServiceImpl(star_url=star_url, resource_url=resource_url)
  inner = LiquidHandlerServiceASGIApplication(svc)

  @asynccontextmanager
  async def _lifespan(app: Any):
    await svc._lh.setup()
    yield
    await svc._lh.stop()

  async def app(scope: dict, receive: Any, send: Any) -> None:
    if scope["type"] == "lifespan":
      async with _lifespan(app):
        while True:
          message = await receive()
          if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})
          elif message["type"] == "lifespan.shutdown":
            break
      await send({"type": "lifespan.shutdown.complete"})
    else:
      await inner(scope, receive, send)

  return app
