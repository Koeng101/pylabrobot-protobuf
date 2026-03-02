from typing import ClassVar, Optional

from google.protobuf import descriptor, message

DESCRIPTOR: descriptor.FileDescriptor

class Empty(message.Message):
  __slots__ = ()
  def __init__(self) -> None: ...

class Coordinate(message.Message):
  __slots__ = ("x", "y", "z")
  X_FIELD_NUMBER: ClassVar[int]
  Y_FIELD_NUMBER: ClassVar[int]
  Z_FIELD_NUMBER: ClassVar[int]
  x: float
  y: float
  z: float
  def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ...) -> None: ...

class Rotation(message.Message):
  __slots__ = ("x", "y", "z")
  X_FIELD_NUMBER: ClassVar[int]
  Y_FIELD_NUMBER: ClassVar[int]
  Z_FIELD_NUMBER: ClassVar[int]
  x: float
  y: float
  z: float
  def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ...) -> None: ...
