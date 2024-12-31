files = env_get
test_files = *

# For local development
test:
	pytest -s -v test/test_$(test_files).py --doctest-modules --cov env_get --cov-config=.coveragerc --cov-report term-missing

# For github actions
test-ci:
	pytest -s -v test/test_$(test_files).py --doctest-modules --cov env_get --cov-config=.coveragerc --cov-report=xml

lint:
	@echo "Running ruff..."
	@ruff check $(files)
	@echo "Running mypy..."
	@mypy $(files)

fix:
	ruff check --fix $(files)

install:
	pip install -U .[dev]

install-all:
	pip install -U .[dev,doc]

report:
	codecov

build: env_get
	rm -rf dist
	python -m build

publish:
	make build
	twine upload --config-file ~/.pypirc -r pypi dist/*

.PHONY: test build
