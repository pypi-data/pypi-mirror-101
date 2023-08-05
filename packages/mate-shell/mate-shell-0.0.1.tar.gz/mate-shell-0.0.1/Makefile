help:
	@echo ""
	@echo "Available commands"
	@echo ""
	@echo " - install      : installs mate as bash command"
	@echo " - flake        : runs flake8 style checks"
	@echo " - black        : format the code"
	@echo " - check        : runs all checks (tests + style)"
	@echo " - pre-commit   : runs pre-commit tests"
	@echo " - clean        : cleans up all folders"
	@echo ""

install:
	pip install -e .

black:
	black .

flake:
	flake8

test:
	pytest --cov=mate --cov-report term --cov-report xml:cov.xml

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf __pycache__ .pytest_cache

check: black flake test
