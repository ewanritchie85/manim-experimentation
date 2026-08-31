.PHONY: env install system-deps test lint format run run-test run-vector run-maths render-test render-vector render-maths clean ci

env:
	@if [ ! -d .venv ]; then \
		echo "Creating .venv..."; \
		python3 -m venv .venv; \
	else \
		echo ".venv already exists"; \
	fi
	@if [ ! -f .env ] && [ -f .env.example ]; then \
		echo "Copying .env.example to .env..."; \
		cp .env.example .env; \
	elif [ -f .env ]; then \
		echo ".env already exists"; \
	else \
		echo "No .env.example found — skipping .env creation"; \
	fi

system-deps:
	@if command -v apt-get >/dev/null 2>&1; then \
		echo "Installing Linux system dependencies (apt-get)..."; \
		sudo apt-get update && sudo apt-get install -y \
			build-essential \
			python3-dev \
			pkg-config \
			libcairo2-dev \
			libpango1.0-dev \
			libgl1-mesa-dev \
			ffmpeg \
			texlive-latex-base \
			texlive-latex-extra \
			texlive-fonts-recommended \
			texlive-latex-recommended \
			texlive-fonts-extra \
			dvisvgm \
			tipa; \
	elif command -v brew >/dev/null 2>&1; then \
		echo "Installing macOS system dependencies (brew)..."; \
		brew list pango >/dev/null 2>&1 || brew install pango cairo pkg-config ffmpeg; \
	else \
		echo "No supported system package manager found — skipping system-deps"; \
	fi

install: env
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install pytest ruff

test:
	.venv/bin/python -m pytest tests/ -v

lint:
	.venv/bin/ruff check .

format:
	.venv/bin/ruff format .

run:
	.venv/bin/python main.py

run-test:
	.venv/bin/python main.py test

run-vector:
	.venv/bin/python main.py vector

run-maths:
	.venv/bin/python main.py maths

# Direct manim CLI (useful for preview flags like -pql)
render-test:
	.venv/bin/manim -pql scenes/test_scene.py TestScene

render-vector:
	.venv/bin/manim -pql scenes/vector_field.py VectorFieldCurlDivergence

render-maths:
	.venv/bin/manim -pql scenes/maths_tour.py MathShowcase

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache
	rm -rf media/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

ci: system-deps install lint test