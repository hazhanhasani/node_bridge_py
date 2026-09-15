"""Tor multi-exit extension methods for BluePanel Node bridge transports."""

from __future__ import annotations

from collections.abc import Callable

from PasarGuardNodeBridge.common import service_pb2 as service


def _id_request(location_id: str) -> service.TorLocationIDRequest:
    if not location_id:
        raise ValueError("location_id is required")
    return service.TorLocationIDRequest(id=location_id)


async def _grpc_call(self, method: Callable, request, timeout: int | None = None):
    timeout = timeout or max(self._internal_timeout, 30)
    return await self._handle_grpc_request(method=method, request=request, timeout=timeout)


async def grpc_list_tor_locations(self, timeout: int | None = None):
    return await _grpc_call(self, self._client.ListTorLocations, service.Empty(), timeout)


async def grpc_get_tor_location(self, location_id: str, timeout: int | None = None):
    return await _grpc_call(self, self._client.GetTorLocation, _id_request(location_id), timeout)


async def grpc_create_tor_location(self, spec: service.TorLocationSpec, timeout: int | None = None):
    return await _grpc_call(self, self._client.CreateTorLocation, spec, timeout)


async def grpc_update_tor_location(self, spec: service.TorLocationSpec, timeout: int | None = None):
    return await _grpc_call(self, self._client.UpdateTorLocation, spec, timeout)


async def grpc_delete_tor_location(
    self,
    location_id: str,
    purge_data: bool = False,
    timeout: int | None = None,
):
    return await _grpc_call(
        self,
        self._client.DeleteTorLocation,
        service.DeleteTorLocationRequest(id=location_id, purge_data=purge_data),
        timeout,
    )


async def _grpc_id_action(self, rpc_name: str, location_id: str, timeout: int | None = None):
    return await _grpc_call(self, getattr(self._client, rpc_name), _id_request(location_id), timeout)


async def grpc_enable_tor_location(self, location_id: str, timeout: int | None = None):
    return await _grpc_id_action(self, "EnableTorLocation", location_id, timeout)


async def grpc_disable_tor_location(self, location_id: str, timeout: int | None = None):
    return await _grpc_id_action(self, "DisableTorLocation", location_id, timeout)


async def grpc_restart_tor_location(self, location_id: str, timeout: int | None = None):
    return await _grpc_id_action(self, "RestartTorLocation", location_id, timeout)


async def grpc_new_tor_identity(self, location_id: str, timeout: int | None = None):
    return await _grpc_id_action(self, "NewTorIdentity", location_id, timeout)


async def grpc_get_tor_health(self, location_id: str, timeout: int | None = None):
    return await _grpc_id_action(self, "GetTorHealth", location_id, timeout)


async def grpc_repair_tor_location(self, location_id: str, timeout: int | None = None):
    return await _grpc_id_action(self, "RepairTorLocation", location_id, timeout)


async def grpc_test_tor_location(self, location_id: str, timeout: int | None = None):
    return await _grpc_id_action(self, "TestTorLocation", location_id, timeout)


async def grpc_force_reconcile_tor(self, timeout: int | None = None):
    return await _grpc_call(self, self._client.ForceReconcileTor, service.Empty(), timeout)


async def _rest_call(
    self,
    method: str,
    endpoint: str,
    request,
    response_class,
    timeout: int | None = None,
):
    timeout = timeout or max(self._internal_timeout, 30)
    return await self._make_request(
        method=method,
        endpoint=endpoint,
        timeout=timeout,
        proto_message=request,
        proto_response_class=response_class,
    )


async def rest_list_tor_locations(self, timeout: int | None = None):
    return await _rest_call(
        self,
        "GET",
        "tor/locations",
        service.Empty(),
        service.TorLocationsResponse,
        timeout,
    )


async def rest_get_tor_location(self, location_id: str, timeout: int | None = None):
    return await _rest_call(
        self,
        "GET",
        f"tor/locations/{location_id}/",
        service.Empty(),
        service.TorLocation,
        timeout,
    )


async def rest_create_tor_location(self, spec: service.TorLocationSpec, timeout: int | None = None):
    return await _rest_call(self, "POST", "tor/locations", spec, service.TorLocation, timeout)


async def rest_update_tor_location(self, spec: service.TorLocationSpec, timeout: int | None = None):
    if not spec.id:
        raise ValueError("spec.id is required")
    return await _rest_call(
        self,
        "PUT",
        f"tor/locations/{spec.id}/",
        spec,
        service.TorLocation,
        timeout,
    )


async def rest_delete_tor_location(
    self,
    location_id: str,
    purge_data: bool = False,
    timeout: int | None = None,
):
    if not location_id:
        raise ValueError("location_id is required")
    endpoint = f"tor/locations/{location_id}/?purge_data={'true' if purge_data else 'false'}"
    return await _rest_call(self, "DELETE", endpoint, service.Empty(), service.Empty, timeout)


async def _rest_id_action(self, action: str, location_id: str, timeout: int | None = None):
    if not location_id:
        raise ValueError("location_id is required")
    return await _rest_call(
        self,
        "POST",
        f"tor/locations/{location_id}/{action}",
        service.Empty(),
        service.TorLocation,
        timeout,
    )


async def rest_enable_tor_location(self, location_id: str, timeout: int | None = None):
    return await _rest_id_action(self, "enable", location_id, timeout)


async def rest_disable_tor_location(self, location_id: str, timeout: int | None = None):
    return await _rest_id_action(self, "disable", location_id, timeout)


async def rest_restart_tor_location(self, location_id: str, timeout: int | None = None):
    return await _rest_id_action(self, "restart", location_id, timeout)


async def rest_new_tor_identity(self, location_id: str, timeout: int | None = None):
    return await _rest_id_action(self, "new-identity", location_id, timeout)


async def rest_get_tor_health(self, location_id: str, timeout: int | None = None):
    return await _rest_id_action(self, "health", location_id, timeout)


async def rest_repair_tor_location(self, location_id: str, timeout: int | None = None):
    return await _rest_id_action(self, "repair", location_id, timeout)


async def rest_test_tor_location(self, location_id: str, timeout: int | None = None):
    return await _rest_id_action(self, "test", location_id, timeout)


async def rest_force_reconcile_tor(self, timeout: int | None = None):
    return await _rest_call(
        self,
        "POST",
        "tor/reconcile",
        service.Empty(),
        service.TorReconcileResponse,
        timeout,
    )


def install_tor_methods(grpc_node_cls, rest_node_cls) -> None:
    grpc_methods = {
        "list_tor_locations": grpc_list_tor_locations,
        "get_tor_location": grpc_get_tor_location,
        "create_tor_location": grpc_create_tor_location,
        "update_tor_location": grpc_update_tor_location,
        "delete_tor_location": grpc_delete_tor_location,
        "enable_tor_location": grpc_enable_tor_location,
        "disable_tor_location": grpc_disable_tor_location,
        "restart_tor_location": grpc_restart_tor_location,
        "new_tor_identity": grpc_new_tor_identity,
        "get_tor_health": grpc_get_tor_health,
        "repair_tor_location": grpc_repair_tor_location,
        "test_tor_location": grpc_test_tor_location,
        "force_reconcile_tor": grpc_force_reconcile_tor,
    }
    rest_methods = {
        "list_tor_locations": rest_list_tor_locations,
        "get_tor_location": rest_get_tor_location,
        "create_tor_location": rest_create_tor_location,
        "update_tor_location": rest_update_tor_location,
        "delete_tor_location": rest_delete_tor_location,
        "enable_tor_location": rest_enable_tor_location,
        "disable_tor_location": rest_disable_tor_location,
        "restart_tor_location": rest_restart_tor_location,
        "new_tor_identity": rest_new_tor_identity,
        "get_tor_health": rest_get_tor_health,
        "repair_tor_location": rest_repair_tor_location,
        "test_tor_location": rest_test_tor_location,
        "force_reconcile_tor": rest_force_reconcile_tor,
    }
    for name, fn in grpc_methods.items():
        setattr(grpc_node_cls, name, fn)
    for name, fn in rest_methods.items():
        setattr(rest_node_cls, name, fn)
