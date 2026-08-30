# Manim Test Project

A basic Manim animation project demonstrating core concepts including LaTeX math rendering.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
Output files will be created in the `media/` directory.

```bash
python main.py
```

Or with manim CLI:
```bash
manim -pql main.py TestScene
```

## Scenes

- `TestScene` - Demonstrates text, shapes, transforms, grouping, fading, **LaTeX math rendering**

## CI/CD

GitHub Actions workflow runs on push/PR to main:
```bash
make ci
```
Runs: install → lint (ruff) → test (pytest)

## Requirements

- Python 3.11+
- LaTeX with dvisvgm (for MathTex) - MacTeX on macOS, TeX Live on Linux