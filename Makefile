# Config
OSNAME			:= $(shell uname)

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif


all: lint unit functional docs

export PYTHONPATH		:= ${PWD}
export PYTHONASYNCIODEBUG	:=1

dependencies:
	@pip install -U pip
	@pip install pipenv
	@pipenv install --dev

test: lint unit functional pyopenssl

lint: prepare
	@echo "Checking code style ..."
	@pipenv run flake8 --show-source httpretty tests

unit: prepare
	@echo "Running unit tests ..."
	@pipenv run nosetests --cover-erase tests/$@

functional: prepare
	@echo "Running functional tests ..."
	@pipenv run nosetests --cover-erase tests/$@

pyopenssl: prepare
	@echo "Running PyOpenSSL mocking tests ..."
	@pipenv install pyOpenSSL==16.1.0
	@pipenv install ndg-httpsclient==0.4.2
	@pipenv run nosetests --rednose -x --with-coverage --cover-package=httpretty -s tests/pyopenssl

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; done
	@echo "OK!"
	@printf "Deleting built documentation"
	@rm -rf docs/build
	@printf "Deleting dist files"
	@rm -rf dist

release: lint unit functional docs
	@rm -rf dist/*
	@./.release
	@make pypi

pypi:
	@pipenv run python setup.py build sdist
	@pipenv run twine upload dist/*.tar.gz

docs:
	@cd docs && make html
	$(OPEN_COMMAND) docs/build/html/index.html

prepare:
	@reset


.PHONY: docs
