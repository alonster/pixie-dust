# PixieDust

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Textual-ff4757.svg)](https://textual.textualize.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

`pixie-dust` is a lightweight, interactive Hex Editor
built with the [Textualize/textual](https://github.com/Textualize/textual) framework
and inspired by [`hexyl`](https://github.com/sharkdp/hexyl).
It’s designed for low-level data analysis and quick binary prototyping directly from your favorite terminal.

## Installation

In order to install `pixie-dust` from source:

```bash
# Clone the repository
git clone https://github.com/alonster/pixie-dust.git
cd pixie-dust

# Sync dependencies ('--no-dev' is optional)
uv sync --no-dev

# Install pixie-dust
uv pip install --editable .
```

`pixie-dust` uses `uv` as its package manager, so make sure is it installed.

## Usage

To run `pixie-dust`, simply run:

```bash
uv run pixie-dust demo.bin
```

## Develop and Test

If you want to test the app or a new feature, you can run:

```bash
uv run pytest
```

Note: `uv` will automatically install development-related dependencies.

Feel free to add more tests under the `test/` directory.
