"""Client stubs for lifecycle operations (Setup, Stop, capability queries)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._generated import star_service_pb2 as pb2

if TYPE_CHECKING:
  from ._generated.star_service_connect import STARServiceClient, STARServiceClientSync


class LifecycleClientMixin:
  _client: STARServiceClient
  _client_sync: STARServiceClientSync
  """Client stubs for lifecycle operations.

  ``self._client`` is a :class:`STARServiceClient` instance.
  """

  def set_deck(self, deck: Any) -> None:
    # No-op: the real deck lives on the remote STAR service.
    pass

  def set_heads(self, head: Any = None, head96: Any = None) -> None:
    # No-op: heads live on the remote STAR service.
    pass

  @property
  def head96_installed(self) -> bool:
    return self.core96_head_installed

  @property
  def num_arms(self) -> int:
    return 1 if self.iswap_installed else 0

  async def setup(self) -> None:
    await self._client.setup(pb2.SetupRequest())

  async def stop(self) -> None:
    await self._client.stop(pb2.StopRequest())

  @property
  def num_channels(self) -> int:
    resp = self._client_sync.get_num_channels(pb2.GetNumChannelsRequest())
    return resp.num_channels

  @property
  def core96_head_installed(self) -> bool:
    resp = self._client_sync.get_head96_installed(pb2.GetHead96InstalledRequest())
    return resp.installed

  @property
  def iswap_installed(self) -> bool:
    resp = self._client_sync.get_iswap_installed(pb2.GetIswapInstalledRequest())
    return resp.installed

  @property
  def iswap_parked(self) -> bool:
    resp = self._client_sync.get_iswap_parked(pb2.GetIswapParkedRequest())
    return resp.parked

  @property
  def core_parked(self) -> bool:
    resp = self._client_sync.get_core_parked(pb2.GetCoreParkedRequest())
    return resp.parked
