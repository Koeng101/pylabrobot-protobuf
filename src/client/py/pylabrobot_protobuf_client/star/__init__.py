"""RemoteSTARBackend client implementation combining all mixins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._autoload import AutoloadClientMixin
from ._channel import ChannelClientMixin
from ._core_gripper import CoreGripperClientMixin
from ._generated.star_service_connect import STARServiceClient, STARServiceClientSync
from ._head96 import Head96ClientMixin
from ._iswap import IswapClientMixin
from ._lifecycle import LifecycleClientMixin
from ._misc import MiscClientMixin
from ._pipetting import PipettingClientMixin

if TYPE_CHECKING:
  pass


class RemoteSTARBackend(
  PipettingClientMixin,
  ChannelClientMixin,
  Head96ClientMixin,
  IswapClientMixin,
  CoreGripperClientMixin,
  AutoloadClientMixin,
  MiscClientMixin,
  LifecycleClientMixin,
):
  """ConnectRPC client that acts as a drop-in replacement for STARBackend."""

  def __init__(self, client: STARServiceClient, client_sync: STARServiceClientSync):
    super().__init__()
    self._client = client
    self._client_sync = client_sync

  @classmethod
  def connect(cls, base_url: str = "http://localhost:8080") -> "RemoteSTARBackend":
    """Create a RemoteSTARBackend connected to a remote STAR service."""
    client = STARServiceClient(address=base_url)
    client_sync = STARServiceClientSync(address=base_url)
    return cls(client, client_sync)
