# Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/Picnic-DoC/meegflow).

## Development setup

```bash
git clone https://github.com/Picnic-DoC/meegflow.git
cd meegflow
pip install -e ".[dev]"
```

## Running tests

```bash
pytest tests/
```

## Building the docs locally

```bash
pip install mkdocs-material mkdocstrings[python]
mkdocs serve
```

Then open `http://127.0.0.1:8000` in your browser.
