"""
BluePanel Node Bridge legacy compatibility implementation.

New BluePanel code should import ``BluePanelNodeBridge``. This historical
module path remains available as a compatibility layer for existing deployments.

Version: 0.10.0
"""

__version__ = "0.10.0"
__author__ = "BluePanel"

from enum import Enum

from PasarGuardNodeBridge.abstract_node import PasarGuardNode
from PasarGuardNodeBridge.controller import Health, NodeAPIError
from PasarGuardNodeBridge.grpclib import Node as GrpcNode
from PasarGuardNodeBridge.rest import Node as RestNode
from PasarGuardNodeBridge.storage import (
    ClaimedUser,
    InMemoryNodeLifecycleCoordinator,
    InMemoryNodeRegistry,
    InMemoryUserSyncStore,
    LifecycleLease,
    LifecycleOperation,
    LifecycleStatus,
    NodeConfig,
    NodeLifecycleCoordinatorProtocol,
    NodeLifecycleState,
    NodeRegistryProtocol,
    UserSyncStoreProtocol,
)
from PasarGuardNodeBridge.utils import create_proxy, create_user


class NodeType(str, Enum):
    grpc = "grpc"
    rest = "rest"


def create_node(
    connection: NodeType,
    address: str,
    port: int,
    server_ca: str,
    api_key: str,
    **kwargs,
) -> PasarGuardNode:
    """Create and initialize a BluePanel Node bridge client."""
    if connection is NodeType.grpc:
        return GrpcNode(address=address, port=port, server_ca=server_ca, api_key=api_key, **kwargs)
    if connection is NodeType.rest:
        return RestNode(address=address, port=port, server_ca=server_ca, api_key=api_key, **kwargs)
    raise ValueError("invalid backend type")


def create_node_from_config(config: NodeConfig, **runtime_overrides) -> PasarGuardNode:
    data = config.to_dict()
    data.update(runtime_overrides)
    connection = NodeType(data.pop("connection"))
    return create_node(connection=connection, **data)


async def save_node_config(registry: NodeRegistryProtocol, node_id: str, config: NodeConfig) -> None:
    await registry.upsert_node(node_id, config)


async def create_node_from_registry(
    registry: NodeRegistryProtocol, node_id: str, **runtime_overrides
) -> PasarGuardNode:
    config = await registry.get_node(node_id)
    if config is None:
        raise KeyError(f"Node config not found: {node_id}")
    return create_node_from_config(config, node_id=node_id, **runtime_overrides)


__all__ = [
    "ClaimedUser",
    "Health",
    "InMemoryNodeLifecycleCoordinator",
    "InMemoryNodeRegistry",
    "InMemoryUserSyncStore",
    "LifecycleLease",
    "LifecycleOperation",
    "LifecycleStatus",
    "NodeAPIError",
    "NodeConfig",
    "NodeLifecycleCoordinatorProtocol",
    "NodeLifecycleState",
    "NodeRegistryProtocol",
    "NodeType",
    "PasarGuardNode",
    "UserSyncStoreProtocol",
    "create_node",
    "create_node_from_config",
    "create_node_from_registry",
    "create_proxy",
    "create_user",
    "save_node_config",
]
