"""Minimal stand-in for the Atlas issuer-relay router (DEMO only).

Mimics the shape of the real service so the Remediation Agent's fix
(switching active_relay_path primary -> secondary) applies to real code
and real tests, without needing the client's actual codebase.
"""
from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "atlas" / "relay-routing.yaml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def active_path(config: dict) -> dict:
    """Return the routing path config currently marked active."""
    key = config["active_relay_path"]
    if key not in config["paths"]:
        raise ValueError(f"active_relay_path '{key}' is not defined in paths")
    return config["paths"][key]


def route_auth(issuer_code: str, config: dict | None = None) -> dict:
    """Route an authorization for an issuer down the active relay path."""
    config = config or load_config()
    if issuer_code not in config["issuers"]:
        raise KeyError(f"unknown issuer: {issuer_code}")
    path = active_path(config)
    return {
        "issuer": issuer_code,
        "relay_host": path["host"],
        "timeout_ms": path["timeout_ms"],
        "action_code": "000",  # success marker once routed to a healthy path
    }
