"""RemoteLiquidHandler — string-based client for the LiquidHandlerService."""

from __future__ import annotations

from typing import Optional

from ._generated import liquid_handler_service_pb2 as pb2
from ._generated.liquid_handler_service_connect import LiquidHandlerServiceClientSync

# Re-export for convenience.
GripDirection = pb2.GripDirection
GRIP_DIRECTION_FRONT = pb2.GRIP_DIRECTION_FRONT
GRIP_DIRECTION_BACK = pb2.GRIP_DIRECTION_BACK
GRIP_DIRECTION_LEFT = pb2.GRIP_DIRECTION_LEFT
GRIP_DIRECTION_RIGHT = pb2.GRIP_DIRECTION_RIGHT


class RemoteLiquidHandler:
  """Client for LiquidHandlerService that references resources by name.

  All resource parameters are plain strings, making this suitable for
  cross-language clients that don't have access to pylabrobot objects.

  Usage::

      lh = RemoteLiquidHandler.connect("http://localhost:8082")
      lh.setup(star_url="http://localhost:8080", resource_url="http://localhost:8081")
      lh.pick_up_tips(["tip_rack_0_A1", "tip_rack_0_B1"])
      lh.aspirate(["plate_0_A1", "plate_0_B1"], vols=[50.0, 50.0])
      lh.dispense(["plate_0_A2", "plate_0_B2"], vols=[50.0, 50.0])
      lh.drop_tips(["tip_rack_0_A1", "tip_rack_0_B1"])
      lh.stop()
  """

  def __init__(self, client: LiquidHandlerServiceClientSync) -> None:
    self._client = client

  @classmethod
  def connect(cls, base_url: str = "http://localhost:8082") -> RemoteLiquidHandler:
    """Connect to a remote LiquidHandler service.

    Args:
        base_url: The HTTP URL of the LiquidHandler server.
    """
    return cls(LiquidHandlerServiceClientSync(address=base_url))

  # --- Lifecycle ---

  def setup(self, star_url: str, resource_url: str) -> None:
    """Connect to STAR and Resource servers and set up the LiquidHandler."""
    self._client.setup(pb2.SetupRequest(star_url=star_url, resource_url=resource_url))

  def stop(self) -> None:
    """Tear down the LiquidHandler and disconnect from backend servers."""
    self._client.stop(pb2.Empty())

  # --- Single-channel tips ---

  def pick_up_tips(
    self,
    tip_spot_names: list[str],
    use_channels: Optional[list[int]] = None,
    offsets: Optional[list[tuple[float, float, float]]] = None,
  ) -> None:
    """Pick up tips from the given tip spots."""
    req = pb2.PickUpTipsRequest(tip_spot_names=tip_spot_names)
    if use_channels is not None:
      req.use_channels.extend(use_channels)
    if offsets is not None:
      req.offsets.extend(pb2.Coordinate(x=x, y=y, z=z) for x, y, z in offsets)
    self._client.pick_up_tips(req)

  def drop_tips(
    self,
    tip_spot_names: list[str],
    use_channels: Optional[list[int]] = None,
    offsets: Optional[list[tuple[float, float, float]]] = None,
    allow_nonzero_volume: bool = False,
  ) -> None:
    """Drop tips into the given tip spots or trash."""
    req = pb2.DropTipsRequest(
      tip_spot_names=tip_spot_names,
      allow_nonzero_volume=allow_nonzero_volume,
    )
    if use_channels is not None:
      req.use_channels.extend(use_channels)
    if offsets is not None:
      req.offsets.extend(pb2.Coordinate(x=x, y=y, z=z) for x, y, z in offsets)
    self._client.drop_tips(req)

  def return_tips(
    self,
    use_channels: Optional[list[int]] = None,
    allow_nonzero_volume: bool = False,
    offsets: Optional[list[tuple[float, float, float]]] = None,
  ) -> None:
    """Return tips to the spots they were originally picked up from."""
    req = pb2.ReturnTipsRequest(allow_nonzero_volume=allow_nonzero_volume)
    if use_channels is not None:
      req.use_channels.extend(use_channels)
    if offsets is not None:
      req.offsets.extend(pb2.Coordinate(x=x, y=y, z=z) for x, y, z in offsets)
    self._client.return_tips(req)

  def discard_tips(
    self,
    use_channels: Optional[list[int]] = None,
    allow_nonzero_volume: bool = True,
    offsets: Optional[list[tuple[float, float, float]]] = None,
  ) -> None:
    """Discard tips into the trash."""
    req = pb2.DiscardTipsRequest(allow_nonzero_volume=allow_nonzero_volume)
    if use_channels is not None:
      req.use_channels.extend(use_channels)
    if offsets is not None:
      req.offsets.extend(pb2.Coordinate(x=x, y=y, z=z) for x, y, z in offsets)
    self._client.discard_tips(req)

  # --- Single-channel liquid ---

  def aspirate(
    self,
    resource_names: list[str],
    vols: list[float],
    use_channels: Optional[list[int]] = None,
    flow_rates: Optional[list[Optional[float]]] = None,
    offsets: Optional[list[tuple[float, float, float]]] = None,
    liquid_height: Optional[list[Optional[float]]] = None,
    blow_out_air_volume: Optional[list[Optional[float]]] = None,
  ) -> None:
    """Aspirate liquid from containers."""
    req = pb2.AspirateRequest(resource_names=resource_names, vols=vols)
    if use_channels is not None:
      req.use_channels.extend(use_channels)
    if flow_rates is not None:
      req.flow_rates.extend(
        pb2.OptionalFloat(value=v) if v is not None else pb2.OptionalFloat() for v in flow_rates
      )
    if offsets is not None:
      req.offsets.extend(pb2.Coordinate(x=x, y=y, z=z) for x, y, z in offsets)
    if liquid_height is not None:
      req.liquid_height.extend(
        pb2.OptionalFloat(value=v) if v is not None else pb2.OptionalFloat()
        for v in liquid_height
      )
    if blow_out_air_volume is not None:
      req.blow_out_air_volume.extend(
        pb2.OptionalFloat(value=v) if v is not None else pb2.OptionalFloat()
        for v in blow_out_air_volume
      )
    self._client.aspirate(req)

  def dispense(
    self,
    resource_names: list[str],
    vols: list[float],
    use_channels: Optional[list[int]] = None,
    flow_rates: Optional[list[Optional[float]]] = None,
    offsets: Optional[list[tuple[float, float, float]]] = None,
    liquid_height: Optional[list[Optional[float]]] = None,
    blow_out_air_volume: Optional[list[Optional[float]]] = None,
  ) -> None:
    """Dispense liquid into containers."""
    req = pb2.DispenseRequest(resource_names=resource_names, vols=vols)
    if use_channels is not None:
      req.use_channels.extend(use_channels)
    if flow_rates is not None:
      req.flow_rates.extend(
        pb2.OptionalFloat(value=v) if v is not None else pb2.OptionalFloat() for v in flow_rates
      )
    if offsets is not None:
      req.offsets.extend(pb2.Coordinate(x=x, y=y, z=z) for x, y, z in offsets)
    if liquid_height is not None:
      req.liquid_height.extend(
        pb2.OptionalFloat(value=v) if v is not None else pb2.OptionalFloat()
        for v in liquid_height
      )
    if blow_out_air_volume is not None:
      req.blow_out_air_volume.extend(
        pb2.OptionalFloat(value=v) if v is not None else pb2.OptionalFloat()
        for v in blow_out_air_volume
      )
    self._client.dispense(req)

  # --- 96-head tips ---

  def pick_up_tips96(
    self,
    tip_rack_name: str,
    offset: Optional[tuple[float, float, float]] = None,
  ) -> None:
    """Pick up tips with the 96-channel head from a tip rack."""
    req = pb2.PickUpTips96Request(tip_rack_name=tip_rack_name)
    if offset is not None:
      req.offset.CopyFrom(pb2.Coordinate(x=offset[0], y=offset[1], z=offset[2]))
    self._client.pick_up_tips96(req)

  def drop_tips96(
    self,
    resource_name: str,
    offset: Optional[tuple[float, float, float]] = None,
    allow_nonzero_volume: bool = False,
  ) -> None:
    """Drop tips with the 96-channel head into a tip rack or trash."""
    req = pb2.DropTips96Request(
      resource_name=resource_name,
      allow_nonzero_volume=allow_nonzero_volume,
    )
    if offset is not None:
      req.offset.CopyFrom(pb2.Coordinate(x=offset[0], y=offset[1], z=offset[2]))
    self._client.drop_tips96(req)

  def return_tips96(
    self,
    allow_nonzero_volume: bool = False,
    offset: Optional[tuple[float, float, float]] = None,
  ) -> None:
    """Return 96-head tips to the rack they were originally picked up from."""
    req = pb2.ReturnTips96Request(allow_nonzero_volume=allow_nonzero_volume)
    if offset is not None:
      req.offset.CopyFrom(pb2.Coordinate(x=offset[0], y=offset[1], z=offset[2]))
    self._client.return_tips96(req)

  def discard_tips96(self, allow_nonzero_volume: bool = True) -> None:
    """Discard 96-head tips into the trash."""
    self._client.discard_tips96(pb2.DiscardTips96Request(allow_nonzero_volume=allow_nonzero_volume))

  # --- 96-head liquid ---

  def aspirate96(
    self,
    resource_name: str,
    volume: float,
    offset: Optional[tuple[float, float, float]] = None,
    flow_rate: Optional[float] = None,
    liquid_height: Optional[float] = None,
    blow_out_air_volume: Optional[float] = None,
  ) -> None:
    """Aspirate liquid with the 96-channel head."""
    req = pb2.Aspirate96Request(resource_name=resource_name, volume=volume)
    if offset is not None:
      req.offset.CopyFrom(pb2.Coordinate(x=offset[0], y=offset[1], z=offset[2]))
    if flow_rate is not None:
      req.flow_rate.CopyFrom(pb2.OptionalFloat(value=flow_rate))
    if liquid_height is not None:
      req.liquid_height.CopyFrom(pb2.OptionalFloat(value=liquid_height))
    if blow_out_air_volume is not None:
      req.blow_out_air_volume.CopyFrom(pb2.OptionalFloat(value=blow_out_air_volume))
    self._client.aspirate96(req)

  def dispense96(
    self,
    resource_name: str,
    volume: float,
    offset: Optional[tuple[float, float, float]] = None,
    flow_rate: Optional[float] = None,
    liquid_height: Optional[float] = None,
    blow_out_air_volume: Optional[float] = None,
  ) -> None:
    """Dispense liquid with the 96-channel head."""
    req = pb2.Dispense96Request(resource_name=resource_name, volume=volume)
    if offset is not None:
      req.offset.CopyFrom(pb2.Coordinate(x=offset[0], y=offset[1], z=offset[2]))
    if flow_rate is not None:
      req.flow_rate.CopyFrom(pb2.OptionalFloat(value=flow_rate))
    if liquid_height is not None:
      req.liquid_height.CopyFrom(pb2.OptionalFloat(value=liquid_height))
    if blow_out_air_volume is not None:
      req.blow_out_air_volume.CopyFrom(pb2.OptionalFloat(value=blow_out_air_volume))
    self._client.dispense96(req)

  # --- Resource movement (high-level) ---

  def move_resource(
    self,
    resource_name: str,
    to_name: Optional[str] = None,
    to_coordinate: Optional[tuple[float, float, float]] = None,
    intermediate_locations: Optional[list[tuple[float, float, float]]] = None,
    pickup_offset: Optional[tuple[float, float, float]] = None,
    destination_offset: Optional[tuple[float, float, float]] = None,
    pickup_distance_from_top: float = 0,
    pickup_direction: pb2.GripDirection = pb2.GRIP_DIRECTION_FRONT,
    drop_direction: pb2.GripDirection = pb2.GRIP_DIRECTION_FRONT,
  ) -> None:
    """Move a resource from its current location to a destination."""
    req = pb2.MoveResourceRequest(
      resource_name=resource_name,
      pickup_distance_from_top=pickup_distance_from_top,
      pickup_direction=pickup_direction,
      drop_direction=drop_direction,
    )
    if to_name is not None:
      req.to_name = to_name
    elif to_coordinate is not None:
      req.to_coordinate.CopyFrom(
        pb2.Coordinate(x=to_coordinate[0], y=to_coordinate[1], z=to_coordinate[2])
      )
    if intermediate_locations is not None:
      req.intermediate_locations.extend(
        pb2.Coordinate(x=x, y=y, z=z) for x, y, z in intermediate_locations
      )
    if pickup_offset is not None:
      req.pickup_offset.CopyFrom(
        pb2.Coordinate(x=pickup_offset[0], y=pickup_offset[1], z=pickup_offset[2])
      )
    if destination_offset is not None:
      req.destination_offset.CopyFrom(
        pb2.Coordinate(x=destination_offset[0], y=destination_offset[1], z=destination_offset[2])
      )
    self._client.move_resource(req)

  def move_plate(
    self,
    plate_name: str,
    to_name: Optional[str] = None,
    to_coordinate: Optional[tuple[float, float, float]] = None,
    intermediate_locations: Optional[list[tuple[float, float, float]]] = None,
    pickup_offset: Optional[tuple[float, float, float]] = None,
    destination_offset: Optional[tuple[float, float, float]] = None,
    pickup_direction: pb2.GripDirection = pb2.GRIP_DIRECTION_FRONT,
    drop_direction: pb2.GripDirection = pb2.GRIP_DIRECTION_FRONT,
    pickup_distance_from_top: Optional[float] = None,
  ) -> None:
    """Move a plate (convenience wrapper with plate-specific defaults)."""
    req = pb2.MovePlateRequest(
      plate_name=plate_name,
      pickup_direction=pickup_direction,
      drop_direction=drop_direction,
    )
    if to_name is not None:
      req.to_name = to_name
    elif to_coordinate is not None:
      req.to_coordinate.CopyFrom(
        pb2.Coordinate(x=to_coordinate[0], y=to_coordinate[1], z=to_coordinate[2])
      )
    if intermediate_locations is not None:
      req.intermediate_locations.extend(
        pb2.Coordinate(x=x, y=y, z=z) for x, y, z in intermediate_locations
      )
    if pickup_offset is not None:
      req.pickup_offset.CopyFrom(
        pb2.Coordinate(x=pickup_offset[0], y=pickup_offset[1], z=pickup_offset[2])
      )
    if destination_offset is not None:
      req.destination_offset.CopyFrom(
        pb2.Coordinate(x=destination_offset[0], y=destination_offset[1], z=destination_offset[2])
      )
    if pickup_distance_from_top is not None:
      req.pickup_distance_from_top.CopyFrom(pb2.OptionalFloat(value=pickup_distance_from_top))
    self._client.move_plate(req)

  def move_lid(
    self,
    lid_name: str,
    to_name: Optional[str] = None,
    to_coordinate: Optional[tuple[float, float, float]] = None,
    intermediate_locations: Optional[list[tuple[float, float, float]]] = None,
    pickup_offset: Optional[tuple[float, float, float]] = None,
    destination_offset: Optional[tuple[float, float, float]] = None,
    pickup_direction: pb2.GripDirection = pb2.GRIP_DIRECTION_FRONT,
    drop_direction: pb2.GripDirection = pb2.GRIP_DIRECTION_FRONT,
    pickup_distance_from_top: Optional[float] = None,
  ) -> None:
    """Move a lid (convenience wrapper with lid-specific defaults)."""
    req = pb2.MoveLidRequest(
      lid_name=lid_name,
      pickup_direction=pickup_direction,
      drop_direction=drop_direction,
    )
    if to_name is not None:
      req.to_name = to_name
    elif to_coordinate is not None:
      req.to_coordinate.CopyFrom(
        pb2.Coordinate(x=to_coordinate[0], y=to_coordinate[1], z=to_coordinate[2])
      )
    if intermediate_locations is not None:
      req.intermediate_locations.extend(
        pb2.Coordinate(x=x, y=y, z=z) for x, y, z in intermediate_locations
      )
    if pickup_offset is not None:
      req.pickup_offset.CopyFrom(
        pb2.Coordinate(x=pickup_offset[0], y=pickup_offset[1], z=pickup_offset[2])
      )
    if destination_offset is not None:
      req.destination_offset.CopyFrom(
        pb2.Coordinate(x=destination_offset[0], y=destination_offset[1], z=destination_offset[2])
      )
    if pickup_distance_from_top is not None:
      req.pickup_distance_from_top.CopyFrom(pb2.OptionalFloat(value=pickup_distance_from_top))
    self._client.move_lid(req)

  # --- Resource movement (low-level 3-step) ---

  def pick_up_resource(
    self,
    resource_name: str,
    offset: Optional[tuple[float, float, float]] = None,
    pickup_distance_from_top: Optional[float] = None,
    direction: pb2.GripDirection = pb2.GRIP_DIRECTION_FRONT,
  ) -> None:
    """Pick up a resource with the gripper arm."""
    req = pb2.PickUpResourceRequest(resource_name=resource_name, direction=direction)
    if offset is not None:
      req.offset.CopyFrom(pb2.Coordinate(x=offset[0], y=offset[1], z=offset[2]))
    if pickup_distance_from_top is not None:
      req.pickup_distance_from_top.CopyFrom(pb2.OptionalFloat(value=pickup_distance_from_top))
    self._client.pick_up_resource(req)

  def move_picked_up_resource(
    self,
    to: tuple[float, float, float],
    offset: Optional[tuple[float, float, float]] = None,
    direction: Optional[pb2.GripDirection] = None,
  ) -> None:
    """Move the currently picked-up resource to a new coordinate."""
    req = pb2.MovePickedUpResourceRequest(to=pb2.Coordinate(x=to[0], y=to[1], z=to[2]))
    if offset is not None:
      req.offset.CopyFrom(pb2.Coordinate(x=offset[0], y=offset[1], z=offset[2]))
    if direction is not None:
      req.direction = direction  # type: ignore[assignment]
    self._client.move_picked_up_resource(req)

  def drop_resource(
    self,
    destination_name: Optional[str] = None,
    destination_coordinate: Optional[tuple[float, float, float]] = None,
    offset: Optional[tuple[float, float, float]] = None,
    direction: pb2.GripDirection = pb2.GRIP_DIRECTION_FRONT,
  ) -> None:
    """Drop the currently picked-up resource at a destination."""
    req = pb2.DropResourceRequest(direction=direction)
    if destination_name is not None:
      req.destination_name = destination_name
    elif destination_coordinate is not None:
      req.destination_coordinate.CopyFrom(
        pb2.Coordinate(
          x=destination_coordinate[0], y=destination_coordinate[1], z=destination_coordinate[2]
        )
      )
    if offset is not None:
      req.offset.CopyFrom(pb2.Coordinate(x=offset[0], y=offset[1], z=offset[2]))
    self._client.drop_resource(req)

  # --- State queries ---

  def get_mounted_tips(self) -> list[pb2.TipInfo]:
    """Get the tips currently mounted on each channel of the pipetting head."""
    resp = self._client.get_mounted_tips(pb2.Empty())
    return list(resp.tips)

  def get_picked_up_resource(self) -> Optional[str]:
    """Get the name of the resource currently held by the gripper arm, or None."""
    resp = self._client.get_picked_up_resource(pb2.Empty())
    if resp.has_resource:
      return resp.resource_name
    return None
