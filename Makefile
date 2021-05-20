.PHONY: tests all unit functional clean dependencies tdd docs html purge dist setup

GIT_ROOT		:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCS_ROOT		:= $(GIT_ROOT)/docs
HTML_ROOT		:= $(DOCS_ROOT)/build/html
VENV_ROOT		:= $(GIT_ROOT)/.venv
VENV			?= $(VENV_ROOT)
DOCS_INDEX		:= $(HTML_ROOT)/index.html

export VENV
export PYTHONASYNCIODEBUG	:=1


all: dependencies tests

$(VENV):  # creates $(VENV) folder if does not exist
	python3 -mvenv $(VENV)
	$(VENV)/bin/pip install -U pip setuptools

setup $(VENV)/bin/sphinx-build $(VENV)/bin/twine $(VENV)/bin/nosetests $(VENV)/bin/pytest $(VENV)/bin/python $(VENV)/bin/pip: # installs latest pip
	test -e $(VENV)/bin/pip || make $(VENV)
	$(VENV)/bin/pip install -r development.txt
	$(VENV)/bin/pip install -e .

# Runs the unit and functional tests
tests: unit bugfixes functional pyopenssl


tdd: $(VENV)/bin/nosetests  # runs all tests
	$(VENV)/bin/nosetests tests --with-watch --cover-erase

# Install dependencies
dependencies: | $(VENV)/bin/nosetests

# runs unit tests
unit: $(VENV)/bin/nosetests  # runs only unit tests
	$(VENV)/bin/nosetests --cover-erase tests/unit


pyopenssl: $(VENV)/bin/nosetests
	$(VENV)/bin/nosetests --cover-erase tests/pyopenssl

bugfixes: $(VENV)/bin/nosetests $(VENV)/bin/pytest   # runs tests for specific bugfixes
	$(VENV)/bin/pytest -v --maxfail=1 --mypy tests/bugfixes/pytest
	$(VENV)/bin/nosetests tests/bugfixes/nosetests


# runs functional tests
functional: $(VENV)/bin/nosetests  # runs functional tests
	$(MAKE) bugfixes
	$(VENV)/bin/nosetests tests/functional/bugfixes
	$(VENV)/bin/nosetests tests/functional



$(DOCS_INDEX): $(VENV)/bin/sphinx-build
	cd docs && make html

html: $(DOCS_INDEX) $(VENV)/bin/sphinx-build

docs: $(DOCS_INDEX) $(VENV)/bin/sphinx-build
	open $(DOCS_INDEX)

release: | clean unit functional tests html
	@rm -rf dist/*
	@./.release
	@make pypi

dist: | clean
	$(VENV)/bin/python setup.py build sdist

pypi: dist | $(VENV)/bin/twine
	$(VENV)/bin/twine upload dist/*.tar.gz

# cleanup temp files
clean:
	rm -rf $(HTML_ROOT) build dist


# purge all virtualenv and temp files, causes everything to be rebuilt
# from scratch by other tasks
purge: clean
	rm -rf $(VENV)
