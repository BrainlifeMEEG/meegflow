# MEEGFlow

**A modular, configuration-driven MEEG preprocessing pipeline using MNE-Python.**

MEEGFlow lets you run a full M/EEG preprocessing pipeline by writing a YAML config file — no boilerplate code required. Each step is a named, parameterisable function; you choose which steps to run, in what order, and with what parameters.

## Features

- **Flexible file discovery** — supports BIDS datasets (`BIDSReader`) and custom glob patterns (`GlobReader`)
- **Modular steps** — filtering, ICA, bad-channel detection, epoching, interpolation, and more
- **Configuration-driven** — one YAML file controls the entire pipeline
- **Custom steps** — extend the pipeline with your own Python functions
- **Rich progress bars** — real-time feedback for batch processing
- **Multiple outputs** — clean `.fif` files, JSON reports, and interactive HTML reports

## Quick start

```bash
pip install meegflow

meegflow --bids-root /path/to/bids \
         --config config.yaml \
         --subjects 01 02 \
         --tasks rest
```

See [Installation](installation.md) and [CLI usage](usage/cli.md) for more detail.
