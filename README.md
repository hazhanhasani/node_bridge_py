# BluePanel Node Bridge (Python)

Python bridge used by **BluePanel** to communicate with **BluePanel Node** over gRPC or REST.

Repository: `hazhanhasani/node_bridge_py`

## Install from the BluePanel fork

```bash
pip install "bluepanel-node-bridge @ git+https://github.com/hazhanhasani/node_bridge_py.git@main"
```

## Import

```python
from BluePanelNodeBridge import Health, NodeAPIError, NodeType, BluePanelNode, create_node
from BluePanelNodeBridge.common import service_pb2 as service
```

## Compatibility

The package currently ships a legacy implementation namespace internally so existing deployments can be upgraded without an immediate hard break. New BluePanel code should use `BluePanelNodeBridge` exclusively.

## Development

```bash
uv sync --group dev
uv run pytest
```

## License

See `LICENSE`.
