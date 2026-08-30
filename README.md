# Manim Test Project

A currently purposeless project to experiment with the creation of animations using Manim.

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

- `TestScene` - Demonstrates text, shapes, transforms, grouping, fading