# Config
OSNAME			:= $(shell uname)

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif


all: check_dependencies unit functional

filename=httpretty-`python -c 'import httpretty;print httpretty.version'`.tar.gz

export HTTPRETTY_DEPENDENCIES:= nose sure
export PYTHONPATH:= ${PWD}

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@for dependency in `echo $$HTTPRETTY_DEPENDENCIES`; do \
		pipenv run python -c "import $$dependency" 2>/dev/null || (echo "You must install $$dependency in order to run httpretty's tests" && exit 3) ; \
		done

test: unit functional

lint:
	@echo "Checking code style ..."
	@pipenv run flake8 --show-source --ignore=F821,E901 httpretty

unit: prepare
	@echo "Running unit tests ..."
	@pipenv run nosetests --rednose -x --with-randomly --with-coverage --cover-package=httpretty -s tests/unit

functional: prepare
	@echo "Running functional tests ..."
	@pipenv run nosetests --rednose -x --with-coverage --cover-package=httpretty -s tests/functional

pyopenssl: prepare
	@echo "Running PyOpenSSL mocking tests ..."
	@pipenv install pyOpenSSL==16.1.0
	@pipenv install ndg-httpsclient==0.4.2
	@pipenv run nosetests --rednose -x --with-coverage --cover-package=httpretty -s tests/pyopenssl

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; done
	@echo "OK!"

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
