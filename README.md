# demo_repo — stand-in codebase for the Incident agent's fix + CI/CD demo

This is a **dummy repository we own** — NOT the client's code. It exists so the Remediation
stage of UC-01 can be shown for real (a genuine PR + a real CI run) without needing the
client's actual codebase. The patterns mirror our incident (Atlas issuer-relay failover).

## What's here
| Path | Role in the demo |
|---|---|
| `config/atlas/relay-routing.yaml` | The file the agent's fix edits (`active_relay_path: primary -> secondary`). |
| `src/relay_router.py` | Tiny stand-in service that reads the config and routes auths. |
| `tests/test_relay_router.py` | The "4/4 sandbox tests" the agent runs before deploy. |
| `.github/workflows/ci.yml` | GitHub Actions — runs the tests on every PR (the real CI run). |

## Three ways to use it in a client demo
1. **Simulated (default):** ignore this repo — the prototype's CI/CD console is fully scripted. Zero setup, never breaks.
2. **Real PR (wow moment):** push this folder to a GitHub repo we own. The agent (or we) opens a PR that flips `active_relay_path` to `secondary`; GitHub Actions runs the tests live; show the green checks. Deploy stays mocked/gated.
3. **Run tests locally:** `pip install pyyaml pytest && pytest -q tests/`

## Important framing for the client
"This runs against a representative repository so nothing touches your systems. In production
the agent is pointed at your repo and CI/CD — the flow is identical."
