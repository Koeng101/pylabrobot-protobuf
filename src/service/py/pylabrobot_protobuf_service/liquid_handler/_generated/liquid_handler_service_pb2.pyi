from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from .types_pb2 import Coordinate as Coordinate
from .types_pb2 import Empty as Empty

DESCRIPTOR: _descriptor.FileDescriptor

class GripDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
  __slots__ = ()
  GRIP_DIRECTION_FRONT: _ClassVar[GripDirection]
  GRIP_DIRECTION_BACK: _ClassVar[GripDirection]
  GRIP_DIRECTION_LEFT: _ClassVar[GripDirection]
  GRIP_DIRECTION_RIGHT: _ClassVar[GripDirection]

GRIP_DIRECTION_FRONT: GripDirection
GRIP_DIRECTION_BACK: GripDirection
GRIP_DIRECTION_LEFT: GripDirection
GRIP_DIRECTION_RIGHT: GripDirection

class OptionalFloat(_message.Message):
  __slots__ = ("value",)
  VALUE_FIELD_NUMBER: _ClassVar[int]
  value: float
  def __init__(self, value: _Optional[float] = ...) -> None: ...

class TipInfo(_message.Message):
  __slots__ = ("channel", "has_tip", "total_tip_length", "maximal_volume", "has_filter", "fitting_depth")
  CHANNEL_FIELD_NUMBER: _ClassVar[int]
  HAS_TIP_FIELD_NUMBER: _ClassVar[int]
  TOTAL_TIP_LENGTH_FIELD_NUMBER: _ClassVar[int]
  MAXIMAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
  HAS_FILTER_FIELD_NUMBER: _ClassVar[int]
  FITTING_DEPTH_FIELD_NUMBER: _ClassVar[int]
  channel: int
  has_tip: bool
  total_tip_length: float
  maximal_volume: float
  has_filter: bool
  fitting_depth: float
  def __init__(
    self,
    channel: _Optional[int] = ...,
    has_tip: bool = ...,
    total_tip_length: _Optional[float] = ...,
    maximal_volume: _Optional[float] = ...,
    has_filter: bool = ...,
    fitting_depth: _Optional[float] = ...,
  ) -> None: ...

# ============================================================
# Requests
# ============================================================

class SetupRequest(_message.Message):
  __slots__ = ()
  def __init__(self) -> None: ...

class PickUpTipsRequest(_message.Message):
  __slots__ = ("tip_spot_names", "use_channels", "offsets")
  TIP_SPOT_NAMES_FIELD_NUMBER: _ClassVar[int]
  USE_CHANNELS_FIELD_NUMBER: _ClassVar[int]
  OFFSETS_FIELD_NUMBER: _ClassVar[int]
  tip_spot_names: _containers.RepeatedScalarFieldContainer[str]
  use_channels: _containers.RepeatedScalarFieldContainer[int]
  offsets: _containers.RepeatedCompositeFieldContainer[Coordinate]
  def __init__(
    self,
    tip_spot_names: _Optional[_Iterable[str]] = ...,
    use_channels: _Optional[_Iterable[int]] = ...,
    offsets: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
  ) -> None: ...

class DropTipsRequest(_message.Message):
  __slots__ = ("tip_spot_names", "use_channels", "offsets", "allow_nonzero_volume")
  TIP_SPOT_NAMES_FIELD_NUMBER: _ClassVar[int]
  USE_CHANNELS_FIELD_NUMBER: _ClassVar[int]
  OFFSETS_FIELD_NUMBER: _ClassVar[int]
  ALLOW_NONZERO_VOLUME_FIELD_NUMBER: _ClassVar[int]
  tip_spot_names: _containers.RepeatedScalarFieldContainer[str]
  use_channels: _containers.RepeatedScalarFieldContainer[int]
  offsets: _containers.RepeatedCompositeFieldContainer[Coordinate]
  allow_nonzero_volume: bool
  def __init__(
    self,
    tip_spot_names: _Optional[_Iterable[str]] = ...,
    use_channels: _Optional[_Iterable[int]] = ...,
    offsets: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
    allow_nonzero_volume: bool = ...,
  ) -> None: ...

class ReturnTipsRequest(_message.Message):
  __slots__ = ("use_channels", "allow_nonzero_volume", "offsets")
  USE_CHANNELS_FIELD_NUMBER: _ClassVar[int]
  ALLOW_NONZERO_VOLUME_FIELD_NUMBER: _ClassVar[int]
  OFFSETS_FIELD_NUMBER: _ClassVar[int]
  use_channels: _containers.RepeatedScalarFieldContainer[int]
  allow_nonzero_volume: bool
  offsets: _containers.RepeatedCompositeFieldContainer[Coordinate]
  def __init__(
    self,
    use_channels: _Optional[_Iterable[int]] = ...,
    allow_nonzero_volume: bool = ...,
    offsets: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
  ) -> None: ...

class DiscardTipsRequest(_message.Message):
  __slots__ = ("use_channels", "allow_nonzero_volume", "offsets")
  USE_CHANNELS_FIELD_NUMBER: _ClassVar[int]
  ALLOW_NONZERO_VOLUME_FIELD_NUMBER: _ClassVar[int]
  OFFSETS_FIELD_NUMBER: _ClassVar[int]
  use_channels: _containers.RepeatedScalarFieldContainer[int]
  allow_nonzero_volume: bool
  offsets: _containers.RepeatedCompositeFieldContainer[Coordinate]
  def __init__(
    self,
    use_channels: _Optional[_Iterable[int]] = ...,
    allow_nonzero_volume: bool = ...,
    offsets: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
  ) -> None: ...

class AspirateRequest(_message.Message):
  __slots__ = (
    "resource_names", "vols", "use_channels", "flow_rates", "offsets",
    "liquid_height", "blow_out_air_volume",
  )
  RESOURCE_NAMES_FIELD_NUMBER: _ClassVar[int]
  VOLS_FIELD_NUMBER: _ClassVar[int]
  USE_CHANNELS_FIELD_NUMBER: _ClassVar[int]
  FLOW_RATES_FIELD_NUMBER: _ClassVar[int]
  OFFSETS_FIELD_NUMBER: _ClassVar[int]
  LIQUID_HEIGHT_FIELD_NUMBER: _ClassVar[int]
  BLOW_OUT_AIR_VOLUME_FIELD_NUMBER: _ClassVar[int]
  resource_names: _containers.RepeatedScalarFieldContainer[str]
  vols: _containers.RepeatedScalarFieldContainer[float]
  use_channels: _containers.RepeatedScalarFieldContainer[int]
  flow_rates: _containers.RepeatedCompositeFieldContainer[OptionalFloat]
  offsets: _containers.RepeatedCompositeFieldContainer[Coordinate]
  liquid_height: _containers.RepeatedCompositeFieldContainer[OptionalFloat]
  blow_out_air_volume: _containers.RepeatedCompositeFieldContainer[OptionalFloat]
  def __init__(
    self,
    resource_names: _Optional[_Iterable[str]] = ...,
    vols: _Optional[_Iterable[float]] = ...,
    use_channels: _Optional[_Iterable[int]] = ...,
    flow_rates: _Optional[_Iterable[_Union[OptionalFloat, _Mapping]]] = ...,
    offsets: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
    liquid_height: _Optional[_Iterable[_Union[OptionalFloat, _Mapping]]] = ...,
    blow_out_air_volume: _Optional[_Iterable[_Union[OptionalFloat, _Mapping]]] = ...,
  ) -> None: ...

class DispenseRequest(_message.Message):
  __slots__ = (
    "resource_names", "vols", "use_channels", "flow_rates", "offsets",
    "liquid_height", "blow_out_air_volume",
  )
  RESOURCE_NAMES_FIELD_NUMBER: _ClassVar[int]
  VOLS_FIELD_NUMBER: _ClassVar[int]
  USE_CHANNELS_FIELD_NUMBER: _ClassVar[int]
  FLOW_RATES_FIELD_NUMBER: _ClassVar[int]
  OFFSETS_FIELD_NUMBER: _ClassVar[int]
  LIQUID_HEIGHT_FIELD_NUMBER: _ClassVar[int]
  BLOW_OUT_AIR_VOLUME_FIELD_NUMBER: _ClassVar[int]
  resource_names: _containers.RepeatedScalarFieldContainer[str]
  vols: _containers.RepeatedScalarFieldContainer[float]
  use_channels: _containers.RepeatedScalarFieldContainer[int]
  flow_rates: _containers.RepeatedCompositeFieldContainer[OptionalFloat]
  offsets: _containers.RepeatedCompositeFieldContainer[Coordinate]
  liquid_height: _containers.RepeatedCompositeFieldContainer[OptionalFloat]
  blow_out_air_volume: _containers.RepeatedCompositeFieldContainer[OptionalFloat]
  def __init__(
    self,
    resource_names: _Optional[_Iterable[str]] = ...,
    vols: _Optional[_Iterable[float]] = ...,
    use_channels: _Optional[_Iterable[int]] = ...,
    flow_rates: _Optional[_Iterable[_Union[OptionalFloat, _Mapping]]] = ...,
    offsets: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
    liquid_height: _Optional[_Iterable[_Union[OptionalFloat, _Mapping]]] = ...,
    blow_out_air_volume: _Optional[_Iterable[_Union[OptionalFloat, _Mapping]]] = ...,
  ) -> None: ...

class PickUpTips96Request(_message.Message):
  __slots__ = ("tip_rack_name", "offset")
  TIP_RACK_NAME_FIELD_NUMBER: _ClassVar[int]
  OFFSET_FIELD_NUMBER: _ClassVar[int]
  tip_rack_name: str
  offset: Coordinate
  def __init__(
    self,
    tip_rack_name: _Optional[str] = ...,
    offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
  ) -> None: ...

class DropTips96Request(_message.Message):
  __slots__ = ("resource_name", "offset", "allow_nonzero_volume")
  RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
  OFFSET_FIELD_NUMBER: _ClassVar[int]
  ALLOW_NONZERO_VOLUME_FIELD_NUMBER: _ClassVar[int]
  resource_name: str
  offset: Coordinate
  allow_nonzero_volume: bool
  def __init__(
    self,
    resource_name: _Optional[str] = ...,
    offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    allow_nonzero_volume: bool = ...,
  ) -> None: ...

class ReturnTips96Request(_message.Message):
  __slots__ = ("allow_nonzero_volume", "offset")
  ALLOW_NONZERO_VOLUME_FIELD_NUMBER: _ClassVar[int]
  OFFSET_FIELD_NUMBER: _ClassVar[int]
  allow_nonzero_volume: bool
  offset: Coordinate
  def __init__(
    self,
    allow_nonzero_volume: bool = ...,
    offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
  ) -> None: ...

class DiscardTips96Request(_message.Message):
  __slots__ = ("allow_nonzero_volume",)
  ALLOW_NONZERO_VOLUME_FIELD_NUMBER: _ClassVar[int]
  allow_nonzero_volume: bool
  def __init__(self, allow_nonzero_volume: bool = ...) -> None: ...

class Aspirate96Request(_message.Message):
  __slots__ = ("resource_name", "volume", "offset", "flow_rate", "liquid_height", "blow_out_air_volume")
  RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
  VOLUME_FIELD_NUMBER: _ClassVar[int]
  OFFSET_FIELD_NUMBER: _ClassVar[int]
  FLOW_RATE_FIELD_NUMBER: _ClassVar[int]
  LIQUID_HEIGHT_FIELD_NUMBER: _ClassVar[int]
  BLOW_OUT_AIR_VOLUME_FIELD_NUMBER: _ClassVar[int]
  resource_name: str
  volume: float
  offset: Coordinate
  flow_rate: OptionalFloat
  liquid_height: OptionalFloat
  blow_out_air_volume: OptionalFloat
  def __init__(
    self,
    resource_name: _Optional[str] = ...,
    volume: _Optional[float] = ...,
    offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    flow_rate: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
    liquid_height: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
    blow_out_air_volume: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
  ) -> None: ...

class Dispense96Request(_message.Message):
  __slots__ = ("resource_name", "volume", "offset", "flow_rate", "liquid_height", "blow_out_air_volume")
  RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
  VOLUME_FIELD_NUMBER: _ClassVar[int]
  OFFSET_FIELD_NUMBER: _ClassVar[int]
  FLOW_RATE_FIELD_NUMBER: _ClassVar[int]
  LIQUID_HEIGHT_FIELD_NUMBER: _ClassVar[int]
  BLOW_OUT_AIR_VOLUME_FIELD_NUMBER: _ClassVar[int]
  resource_name: str
  volume: float
  offset: Coordinate
  flow_rate: OptionalFloat
  liquid_height: OptionalFloat
  blow_out_air_volume: OptionalFloat
  def __init__(
    self,
    resource_name: _Optional[str] = ...,
    volume: _Optional[float] = ...,
    offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    flow_rate: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
    liquid_height: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
    blow_out_air_volume: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
  ) -> None: ...

class MoveResourceRequest(_message.Message):
  __slots__ = (
    "resource_name", "to_name", "to_coordinate", "intermediate_locations",
    "pickup_offset", "destination_offset", "pickup_distance_from_top",
    "pickup_direction", "drop_direction",
  )
  RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
  TO_NAME_FIELD_NUMBER: _ClassVar[int]
  TO_COORDINATE_FIELD_NUMBER: _ClassVar[int]
  INTERMEDIATE_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
  PICKUP_OFFSET_FIELD_NUMBER: _ClassVar[int]
  DESTINATION_OFFSET_FIELD_NUMBER: _ClassVar[int]
  PICKUP_DISTANCE_FROM_TOP_FIELD_NUMBER: _ClassVar[int]
  PICKUP_DIRECTION_FIELD_NUMBER: _ClassVar[int]
  DROP_DIRECTION_FIELD_NUMBER: _ClassVar[int]
  resource_name: str
  to_name: str
  to_coordinate: Coordinate
  intermediate_locations: _containers.RepeatedCompositeFieldContainer[Coordinate]
  pickup_offset: Coordinate
  destination_offset: Coordinate
  pickup_distance_from_top: float
  pickup_direction: GripDirection
  drop_direction: GripDirection
  def __init__(
    self,
    resource_name: _Optional[str] = ...,
    to_name: _Optional[str] = ...,
    to_coordinate: _Optional[_Union[Coordinate, _Mapping]] = ...,
    intermediate_locations: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
    pickup_offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    destination_offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    pickup_distance_from_top: _Optional[float] = ...,
    pickup_direction: _Optional[_Union[GripDirection, str]] = ...,
    drop_direction: _Optional[_Union[GripDirection, str]] = ...,
  ) -> None: ...

class MovePlateRequest(_message.Message):
  __slots__ = (
    "plate_name", "to_name", "to_coordinate", "intermediate_locations",
    "pickup_offset", "destination_offset", "pickup_direction", "drop_direction",
    "pickup_distance_from_top",
  )
  PLATE_NAME_FIELD_NUMBER: _ClassVar[int]
  TO_NAME_FIELD_NUMBER: _ClassVar[int]
  TO_COORDINATE_FIELD_NUMBER: _ClassVar[int]
  INTERMEDIATE_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
  PICKUP_OFFSET_FIELD_NUMBER: _ClassVar[int]
  DESTINATION_OFFSET_FIELD_NUMBER: _ClassVar[int]
  PICKUP_DIRECTION_FIELD_NUMBER: _ClassVar[int]
  DROP_DIRECTION_FIELD_NUMBER: _ClassVar[int]
  PICKUP_DISTANCE_FROM_TOP_FIELD_NUMBER: _ClassVar[int]
  plate_name: str
  to_name: str
  to_coordinate: Coordinate
  intermediate_locations: _containers.RepeatedCompositeFieldContainer[Coordinate]
  pickup_offset: Coordinate
  destination_offset: Coordinate
  pickup_direction: GripDirection
  drop_direction: GripDirection
  pickup_distance_from_top: OptionalFloat
  def __init__(
    self,
    plate_name: _Optional[str] = ...,
    to_name: _Optional[str] = ...,
    to_coordinate: _Optional[_Union[Coordinate, _Mapping]] = ...,
    intermediate_locations: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
    pickup_offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    destination_offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    pickup_direction: _Optional[_Union[GripDirection, str]] = ...,
    drop_direction: _Optional[_Union[GripDirection, str]] = ...,
    pickup_distance_from_top: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
  ) -> None: ...

class MoveLidRequest(_message.Message):
  __slots__ = (
    "lid_name", "to_name", "to_coordinate", "intermediate_locations",
    "pickup_offset", "destination_offset", "pickup_direction", "drop_direction",
    "pickup_distance_from_top",
  )
  LID_NAME_FIELD_NUMBER: _ClassVar[int]
  TO_NAME_FIELD_NUMBER: _ClassVar[int]
  TO_COORDINATE_FIELD_NUMBER: _ClassVar[int]
  INTERMEDIATE_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
  PICKUP_OFFSET_FIELD_NUMBER: _ClassVar[int]
  DESTINATION_OFFSET_FIELD_NUMBER: _ClassVar[int]
  PICKUP_DIRECTION_FIELD_NUMBER: _ClassVar[int]
  DROP_DIRECTION_FIELD_NUMBER: _ClassVar[int]
  PICKUP_DISTANCE_FROM_TOP_FIELD_NUMBER: _ClassVar[int]
  lid_name: str
  to_name: str
  to_coordinate: Coordinate
  intermediate_locations: _containers.RepeatedCompositeFieldContainer[Coordinate]
  pickup_offset: Coordinate
  destination_offset: Coordinate
  pickup_direction: GripDirection
  drop_direction: GripDirection
  pickup_distance_from_top: OptionalFloat
  def __init__(
    self,
    lid_name: _Optional[str] = ...,
    to_name: _Optional[str] = ...,
    to_coordinate: _Optional[_Union[Coordinate, _Mapping]] = ...,
    intermediate_locations: _Optional[_Iterable[_Union[Coordinate, _Mapping]]] = ...,
    pickup_offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    destination_offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    pickup_direction: _Optional[_Union[GripDirection, str]] = ...,
    drop_direction: _Optional[_Union[GripDirection, str]] = ...,
    pickup_distance_from_top: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
  ) -> None: ...

class PickUpResourceRequest(_message.Message):
  __slots__ = ("resource_name", "offset", "pickup_distance_from_top", "direction")
  RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
  OFFSET_FIELD_NUMBER: _ClassVar[int]
  PICKUP_DISTANCE_FROM_TOP_FIELD_NUMBER: _ClassVar[int]
  DIRECTION_FIELD_NUMBER: _ClassVar[int]
  resource_name: str
  offset: Coordinate
  pickup_distance_from_top: OptionalFloat
  direction: GripDirection
  def __init__(
    self,
    resource_name: _Optional[str] = ...,
    offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    pickup_distance_from_top: _Optional[_Union[OptionalFloat, _Mapping]] = ...,
    direction: _Optional[_Union[GripDirection, str]] = ...,
  ) -> None: ...

class MovePickedUpResourceRequest(_message.Message):
  __slots__ = ("to", "offset", "direction")
  TO_FIELD_NUMBER: _ClassVar[int]
  OFFSET_FIELD_NUMBER: _ClassVar[int]
  DIRECTION_FIELD_NUMBER: _ClassVar[int]
  to: Coordinate
  offset: Coordinate
  direction: GripDirection
  def __init__(
    self,
    to: _Optional[_Union[Coordinate, _Mapping]] = ...,
    offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    direction: _Optional[_Union[GripDirection, str]] = ...,
  ) -> None: ...

class DropResourceRequest(_message.Message):
  __slots__ = ("destination_name", "destination_coordinate", "offset", "direction")
  DESTINATION_NAME_FIELD_NUMBER: _ClassVar[int]
  DESTINATION_COORDINATE_FIELD_NUMBER: _ClassVar[int]
  OFFSET_FIELD_NUMBER: _ClassVar[int]
  DIRECTION_FIELD_NUMBER: _ClassVar[int]
  destination_name: str
  destination_coordinate: Coordinate
  offset: Coordinate
  direction: GripDirection
  def __init__(
    self,
    destination_name: _Optional[str] = ...,
    destination_coordinate: _Optional[_Union[Coordinate, _Mapping]] = ...,
    offset: _Optional[_Union[Coordinate, _Mapping]] = ...,
    direction: _Optional[_Union[GripDirection, str]] = ...,
  ) -> None: ...

# ============================================================
# Responses
# ============================================================

class GetMountedTipsResponse(_message.Message):
  __slots__ = ("tips",)
  TIPS_FIELD_NUMBER: _ClassVar[int]
  tips: _containers.RepeatedCompositeFieldContainer[TipInfo]
  def __init__(
    self, tips: _Optional[_Iterable[_Union[TipInfo, _Mapping]]] = ...
  ) -> None: ...

class GetPickedUpResourceResponse(_message.Message):
  __slots__ = ("has_resource", "resource_name")
  HAS_RESOURCE_FIELD_NUMBER: _ClassVar[int]
  RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
  has_resource: bool
  resource_name: str
  def __init__(
    self, has_resource: bool = ..., resource_name: _Optional[str] = ...
  ) -> None: ...
