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
- Scenes: `TestScene` (feature tour) + `MathsShowcase` (`scenes/manim_maths_showcase.py` — 6-part tour: Pythagoras → differentiation → integration → Taylor → linear transform → vector field curl/div)

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

### 2026-08-31 - Maths Showcase Refinements + Vector Field Removal
**Scope:** Scene fixes + DX cleanup
**Summary:** Renamed `scenes/maths_tour.py` → `scenes/manim_maths_showcase.py`, `MathShowcase` → `MathsShowcase` (UK spelling throughout: module docstring, intro `A Tour of Classic Maths Concepts, in Maths`, comments). Fixed `section_title()` to accept `MathTex`/`Mobject` subtitle (`use_math_subtitle` flag) and updated Pythagorean subtitle to `MathTex(r"a^2 + b^2 = c^2")`. Fixed `sq_c` to sit flush outward on hypotenuse via outward normal + rotation (`hyp_mid + n_out*c/2`, `theta=arctan2(h_vec)`). Fixed differentiation/integration overlaps via `next_to(..., DOWN)` stacking, moved `n_label` off `graph_label`, kept `limit_formula`/`integral_formula` at `to_edge(UP)` while alive. Replaced Lagrange `f'(x)` with Leibniz `\frac{dy}{dx}` / `\frac{\Delta y}{\Delta x}` in `limit_formula`, `secant_slope_label`, `slope_label`. Removed `outro()` and its `construct()` call. Deleted standalone `scenes/vector_field.py` and all mentions (`main.py` SCENES `vector`/`curl`, `Makefile` `run-vector`/`render-vector`, `README` scenes/run docs, `tests/test_basic.py` vector tests); `MathsShowcase.vector_field_curl_divergence` remains as tour segment 6.
**Why:** Enforce UK spelling, correct LaTeX rendering and classic Pythagorean layout, prevent label collisions, use Leibniz notation, remove unwanted outro, deduplicate vector field (now only inside tour).
**Impact:** `make run` now renders 2 scenes (`test` + `MathsShowcase`); `make run-maths`/`render-maths` updated to `manim_maths_showcase.py`; `make test` 8 passed (was 12); `make lint` clean; snapshot updated to `TestScene` + `MathsShowcase` only.
**Validation:** `python -m py_compile` + `ruff check` pass; `pytest tests/ -v` 8 passed; `grep -R vector_field --exclude-dir=.venv` shows no standalone file refs; `manim -pql` dry-run and `python main.py maths` render 93 anims to `MathsShowcase.mp4`.
**Follow-ups:** None — vector field now only via `MathsShowcase` segment 6.

### 2026-08-31 - Top-Left Anchored Layout + Tour Alias Removal
**Scope:** Scene layout + DX cleanup
**Summary:** Added `MathsShowcase.top_left_stack(*mobjects, buff=0.25, corner_buff=0.4)` helper (VGroup arrange DOWN left-aligned to UL) and standardised all formula/label placement to UL. Shifted `Axes` in `differentiation` (`RIGHT*0.8+DOWN*0.3`), `integration` (`RIGHT*0.9+DOWN*0.3`), `taylor_series` (`scale 0.92` then `RIGHT*0.7+DOWN*0.3`) to keep UL quarter clear. Moved `differentiation` graph_label/limit_formula/secant_slope_label/slope_label into UL stack with fixed `next_to(..., DOWN).align_to(LEFT)` anchors for `always_redraw`; moved `integration` graph_label/integral_formula/n_label into UL stack and `ftc_formula` below `n_label` (UL, consistent with `det_label`); moved `taylor_series` sin label and `P_n(x)` labels to UL (`next_to(sin_label, DOWN, 0.25 + i*0.42)`). Left `linear_transformation` and `vector_field_curl_divergence` as-is (already UL or field-anchored). Removed intentionally-deleted aliases `tour`/`maths_tour`/`maths-tour` from `main.py` SCENES and `tests/test_basic.py` registry (now only `test`/`maths` required, vector/curl also asserted absent); trimmed `README` alias list to `math, showcase, manim_maths_showcase`.
**Why:** Prevent any concurrent UL collision without buff/arrange, keep axes clear of text, maintain eyeline consistency across 2a/2b, align with single top-left convention.
**Impact:** No two concurrent Mobjects share UL without `arrange`/`next_to` buff; `make run` still 2 scenes, `make test` 8 passed, `make lint` clean.
**Validation:** `ruff check` pass; `pytest tests/ -v` 8 passed; manual code review of coordinates/anchors per section confirms no overlap.
**Follow-ups:** None.