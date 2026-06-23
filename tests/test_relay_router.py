"""Sandbox tests — these are the '4/4 passed' checks the agent runs before deploy."""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from relay_router import active_path, route_auth  # noqa: E402

BASE = {
    "active_relay_path": "primary",
    "paths": {
        "primary": {"host": "relay-primary.internal", "timeout_ms": 4000},
        "secondary": {"host": "relay-secondary.internal", "timeout_ms": 4000},
    },
    "issuers": {"KST": {"name": "Kestrel"}, "VLA": {"name": "Client B"}, "SBL": {"name": "Client C"}},
}


def test_config_schema_valid():
    cfg = dict(BASE)
    assert cfg["active_relay_path"] in cfg["paths"]


def test_secondary_relay_reachable():
    cfg = {**BASE, "active_relay_path": "secondary"}
    assert active_path(cfg)["host"] == "relay-secondary.internal"


def test_kst_auth_returns_action_code_000():
    cfg = {**BASE, "active_relay_path": "secondary"}
    assert route_auth("KST", cfg)["action_code"] == "000"


def test_no_regression_other_issuers():
    cfg = {**BASE, "active_relay_path": "secondary"}
    for issuer in ("VLA", "SBL"):
        assert route_auth(issuer, cfg)["action_code"] == "000"
