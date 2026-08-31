# Manim Test Project

A basic Manim animation project demonstrating core concepts including LaTeX math rendering.

## Setup

All common commands are via the `Makefile` (single entry point per `AGENTS.md`):

```bash
make env      # create .venv and .env (if missing)
make install  # create .venv if needed, install deps from requirements.txt (+ pytest, ruff)
make system-deps  # install OS-level deps (cairo, pango, ffmpeg, LaTeX) via apt/brew
```

Manual alternative:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
Output files will be created in the `media/` directory.

```bash
make run                  # all scenes (TestScene + VectorFieldCurlDivergence + MathShowcase)
make run-test             # only TestScene via main.py
make run-vector           # only VectorFieldCurlDivergence via main.py
make run-maths            # only MathShowcase via main.py
# or directly:
.venv/bin/python main.py test
.venv/bin/python main.py vector
.venv/bin/python main.py maths   # aliases: math, tour, maths_tour, showcase
.venv/bin/python main.py all
```

Or with manim CLI:

```bash
.venv/bin/manim -pql scenes/test_scene.py TestScene
.venv/bin/manim -pql scenes/vector_field.py VectorFieldCurlDivergence
.venv/bin/manim -pql scenes/maths_tour.py MathShowcase
# Makefile shortcuts:
make render-test
make render-vector
make render-maths
```

## Development

```bash
make test    # pytest tests/ -v
make lint    # ruff check .
make format  # ruff format .
make clean   # remove caches and media/
make ci      # system-deps → install → lint → test (same as CI)
```

## Scenes

- `TestScene` (`scenes/test_scene.py`) — Concise tour of Manim's main features with on-screen explanations: **Text/Write**, **Shapes/Create**, **Animation/.animate**, **VGroup**, **MathTex**, **Axes/plot**
- `VectorFieldCurlDivergence` (`scenes/vector_field.py`) — Vector field as superposition of two vortices (curl) + source/sink (divergence). Uses `ArrowVectorField`, `StreamLines`, `Axes`, colour by norm; highlights curl >0 / <0 and div >0 / <0 regions. Formula: `\vec{F}(x,y)=sum k_i * (-(y-y_i), x-x_i)/(r_i^2+eps) + sum m_j * (x-x_j, y-y_j)/(r_j^2+eps)`
- `MathShowcase` (`scenes/maths_tour.py`) — Continuous “tour” of 6 classic concepts, each pairing math + Manim toolkit: **1. Pythagorean** (`Polygon`/`Transform` area proof) → **2. Differentiation** (`ValueTracker`/`always_redraw` secant→tangent limit) → **3. Integration** (`Axes.get_riemann_rectangles` → `get_area`, FTC) → **4. Taylor series** (`Axes.plot` successive `sin` approximations via `math.factorial`) → **5. Linear transformation** (`NumberPlane`/`ApplyMatrix`/`Matrix` det) → **6. Vector field** (reused vortex/source `ArrowVectorField` + `StreamLines`). Each segment clears the scene; `section_title()` cards separate them; `outro()` closes.

## CI/CD

GitHub Actions workflow runs on push/PR to main:
```bash
make ci
```
Runs: install → lint (ruff) → test (pytest)

## Requirements

- Python 3.11+
- LaTeX with dvisvgm (for MathTex) - MacTeX on macOS, TeX Live on Linux