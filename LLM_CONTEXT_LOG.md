# LLM Context Log

## Project Overview
Basic Manim animation project with standard Python project structure.

## Architecture
- `main.py` - Entry point
- `scenes/` - Manim scene classes
- `utils/` - Helper functions
- `assets/` - Static assets (images, fonts, etc.)

## Current Snapshot
- Python 3.11+ with Manim 0.21.0
- Virtual environment in `.venv/` (legacy `venv/` kept)
- Dependencies in `requirements.txt`
- Scenes: `TestScene` (feature tour) + `VectorFieldCurlDivergence` (curl/divergence) + `MathShowcase` (6-part tour: Pythagoras → differentiation → integration → Taylor → linear transform → vector field)

## Safety + Auth Boundaries
- No external APIs or secrets required
- Local rendering only

## Active Priorities
- Basic project scaffolding complete
- TestScene demonstrates core Manim concepts + LaTeX math
- CI/CD pipeline with GitHub Actions + Makefile

---

## Change Log Entries

### 2026-08-30 - Project Bootstrap
**Scope:** Full project initialization
**Summary:** Created venv, installed manim, generated requirements.txt, added .gitignore, README.md, .env.example, .env, tests/, .github/workflows/, and this log
**Why:** Establish standard Python project structure per bootstrap protocol
**Impact:** Project ready for development with all scaffolding in place
**Validation:** `pip install -r requirements.txt` succeeds, `python main.py` runs
**Follow-ups:** Add first custom scene in scenes/

### 2026-08-30 - TestScene Added
**Scope:** Scene development
**Summary:** Created test_scene.py with Text, shapes (Square, Circle, Triangle), transformations (shift, rotate, scale, set_fill), grouping (VGroup), and fading. Removed basic_scene.py. Updated main.py to use TestScene.
**Why:** Demonstrate core Manim animation concepts
**Impact:** Working example scene rendering to media/videos/1080p60/TestScene.mp4
**Validation:** `python main.py` renders successfully
**Follow-ups:** Add more complex scenes, explore 3D, camera controls

### 2026-08-30 - Makefile + CI/CD
**Scope:** Developer experience / CI
**Summary:** Added Makefile with targets (install, test, lint, format, run, clean, ci). Created GitHub Actions workflow (.github/workflows/ci.yml) running `make ci` on push/PR to main. Uses pip caching.
**Why:** Automate quality checks, enable CI/CD
**Impact:** `make ci` runs install→lint→test locally and in CI
**Validation:** `make ci` passes locally
**Follow-ups:** Add actual unit tests to tests/

### 2026-08-30 - LaTeX/MathTex Support
**Scope:** Scene enhancement
**Summary:** Enabled MathTex rendering using system dvisvgm (MacTeX). Updated TestScene with Euler's identity, Gaussian integral, Basel problem formulas. Replaced Text with MathTex for math expressions.
**Why:** Demonstrate LaTeX math rendering capability
**Impact:** Professional math typesetting in animations
**Validation:** `python main.py` renders all MathTex correctly
**Follow-ups:** Explore custom LaTeX templates, 3D math rendering

### 2026-08-31 - Vector Field Scene + Project Alignment
**Scope:** Scene + DX + AGENTS.md compliance
**Summary:** Added `scenes/vector_field.py` (VectorFieldCurlDivergence: vortices for curl, source/sink for divergence — ArrowVectorField + StreamLines + Axes, 4 labelled regions). Updated `main.py` to support `test|vector|all` CLI and render both by default. Extended `Makefile` with `.PHONY` env/install/test/lint/format/run/run-test/run-vector/render-test/render-vector/clean/ci and `install: env` using `.venv/bin/pip`. Updated `tests/test_basic.py` with vector field import/instantiation/func/constant tests. Updated `README.md` Run/Scenes docs and `LLM_CONTEXT_LOG.md` snapshot.
**Why:** Include vector field everywhere (main entry, Makefile, tests, docs, CI) and bring project in line with AGENTS.md single-entry Makefile.
**Impact:** `make run` renders both scenes; `make run-vector`/`render-vector` for isolated runs; `make test` covers vector field; `make lint/format` clean.
**Validation:** `make lint` pass, `make test` 8 passed, `python main.py vector` and `test` render to `media/videos/1080p60/` (57 + ~44 anims).
**Follow-ups:** Consider `scenes/__init__.py` re-exports, add 3D stream-lines variant.

### 2026-08-31 - Maths Tour Scene
**Scope:** Scene + DX integration
**Summary:** Added `scenes/maths_tour.py` (`MathShowcase`: 6 segments — Pythagoras, differentiation (ValueTracker secant→tangent), integration (Riemann→area + FTC), Taylor series (`math.factorial` + `Axes.plot`), linear transform (`NumberPlane` + `ApplyMatrix` + `Matrix` det), vector field curl/div (reused vortex/source `ArrowVectorField`/`StreamLines`); `section_title`/`clear_scene`/`outro` helpers). Fixed `np.math.factorial` → `math.factorial` (numpy 2.4) and lint (`F841`, `RUF012`). Wired throughout: `main.py` SCENES `maths/math/tour/maths_tour/showcase` + `all` subprocess loop over `test,vector,maths`; `Makefile` `run-maths`/`render-maths`; `tests/test_basic.py` 4 maths tests (import/segments/field_func/taylor + registry check); `README.md` Run + Scenes; snapshot + changelog.
**Why:** Include maths tour everywhere per request (single-entry Makefile, entry point, tests, docs, CI) and fix runtime/lint blockers.
**Impact:** `make run` now renders 3 scenes in isolated subprocesses; `make run-maths`/`render-maths` for focused work; `make test` 12 passed; `make lint/format` clean.
**Validation:** `ruff check .` pass, `pytest tests/ -v` 12 passed, spot `python -c` field_func + taylor calc + `python main.py maths --help` alias check.
**Follow-ups:** Render full `MathShowcase` (~3 min) on CI opt-in; split segments for preview dev.