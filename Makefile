.PHONY: install test lint format run clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pytest ruff

test:
	pytest tests/ -v || [ $$? -eq 5 ]

lint:
	ruff check .

format:
	ruff format .

run:
	python main.py

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache
	rm -rf media/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

ci: install lint test