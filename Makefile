all:
	python3 main.py
cloc:
	cloc --exclude-dir=venv,venv_dev,.idea,.pytest_cache,.git,__pycache__ .
test:
	pytest
lint:
	flake8
