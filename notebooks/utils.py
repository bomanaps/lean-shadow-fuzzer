"""Shared utilities for loading run data in analysis notebooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file, returning empty dict if missing."""
    if path.is_file():
        return json.loads(path.read_text())
    return {}


def load_run_data(run_dir: str) -> dict[str, Any]:
    """Load all data for a run into a single dict.

    Returns dict with keys: metadata, stats, regions, bandwidths, topology_gml_path.
    """
    rd = Path(run_dir)
    return {
        "metadata": load_json(rd / "run-metadata.json"),
        "stats": load_json(rd / "stats.json"),
        "regions": load_json(rd / "regions.json"),
        "bandwidths": load_json(rd / "bandwidths.json"),
        "topology_gml_path": rd / "topology.gml" if (rd / "topology.gml").exists() else None,
        "run_dir": str(rd),
        "run_id": (
            load_json(rd / "run-metadata.json").get("run_id", rd.name)
            if (rd / "run-metadata.json").is_file()
            else rd.name
        ),
    }
