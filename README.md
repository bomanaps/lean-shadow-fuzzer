# Shadow Fuzzer

Randomized reproducible Shadow network simulation sweeps.

Reads a template config.toml with optional `{min, max}` range values, generates per-run concrete configs with deterministic sampling, and runs Shadow simulations either locally or inside a Docker ARM container.

## Quickstart

```bash
# Install Python dependencies
uv sync

# Copy and edit the example config
cp config.example.docker-arm.toml config.toml

# Run a dry-run to see what would happen
uv run shadow-fuzzer.py --dry-run config.toml

# Run the full sweep
uv run shadow-fuzzer.py config.toml
```

## Analysis Notebooks & Observatory

Each fuzzer run can be analyzed through pre-built Jupyter notebooks rendered as an interactive web site (the "Observatory"). This includes charts for block propagation latency, attestation coverage, chain finality heatmaps, and network topology.

### 1. Install notebook dependencies

The notebooks require additional packages beyond the base fuzzer dependencies:

```bash
uv sync --group notebooks
```

### 2. Enable notebook rendering in your config

Add `render_notebooks = true` to the `[fuzzer]` section of your config:

```toml
[fuzzer]
render_notebooks = true
```

When enabled, the fuzzer automatically renders notebooks after each successful run.

### 3. Render notebooks manually

You can also render notebooks outside the fuzzer loop:

```bash
# Render for a specific run
uv run python scripts/render_notebooks.py --run-dir fuzzer-output/<run-name>

# Re-render all completed runs
uv run python scripts/render_notebooks.py --all
```

### 4. Start the observatory web site

```bash
# Install frontend dependencies (one time)
cd site && npm install

# Start the dev server
npx astro dev --port 4321
```

Open `http://localhost:4321` to browse runs and their analysis notebooks.

## Re-running a single run

Use `--run-index` to re-run a specific run by its 0-based index:

```bash
# Re-run only run index 1 (the 2nd run in the sweep)
uv run shadow-fuzzer.py --run-index 1 config.toml
```

The fuzzer skips existing run directories, so delete the old one first if you want to reuse the same name:

```bash
rm -rf fuzzer-output/big-relaxed-skunk
uv run shadow-fuzzer.py --run-index 1 config.toml
```

## Cleanup

You can clean up previous fuzzer outputs and observatory rendered notebooks:

```bash
# Start the sweep with a completely fresh output directory
# (removes all previous run folders and observatory rendered notebooks,
#  but keeps cached hash-sig keys)
uv run shadow-fuzzer.py --clean-output config.toml
```

## Project Structure

```
├── scripts/               # Shell scripts (genesis, shadow YAML generation)
│   ├── generate-genesis.sh
│   ├── generate-shadow-yaml.sh
│   ├── parse-vc.sh
│   ├── render_notebooks.py  # Notebook execution & rendering
│   └── client-cmds/       # Per-client command templates
├── notebooks/             # Jupyter analysis notebooks
│   ├── analysis.ipynb     # Main analysis notebook (parameterized per run)
│   └── utils.py           # Data loading utilities
├── templates/genesis/     # Genesis template
├── site/                  # Observatory web site (Astro)
│   └── rendered/          # Rendered notebook HTML per run
├── tests/                 # Test suite
├── shadow-fuzzer.py       # Main entry point
├── shadow_fuzzer/         # Package directory containing:
│   ├── generate_shadow_topology.py
│   └── stats_shadow.py
├── config.example.docker-arm.toml # Example configuration
└── config.example.local.toml      # Local runner configuration
```

## Requirements

- Python >= 3.11
- Node.js (for observatory frontend)
- Docker (for ARM-based Shadow runner)
- `yq` (for shell scripts: `brew install yq`)
