"""BluePanel Node Bridge public API.

This namespace is the BluePanel-facing compatibility layer over the bridge
implementation. New BluePanel code should import from ``BluePanelNodeBridge``.
"""

from PasarGuardNodeBridge import *  # noqa: F403
from PasarGuardNodeBridge import PasarGuardNode as BluePanelNode
from PasarGuardNodeBridge import __version__

try:
    del PasarGuardNode
except NameError:
    pass

__author__ = "BluePanel"

__all__ = [
    "BluePanelNode",
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
    "UserSyncStoreProtocol",
    "create_node",
    "create_node_from_config",
    "create_node_from_registry",
    "create_proxy",
    "create_user",
    "save_node_config",
]
