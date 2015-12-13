# Config
OSNAME			:= $(shell uname)

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif


all: check_dependencies unit functional acceptance

filename=httpretty-`python -c 'import httpretty;print httpretty.version'`.tar.gz

export HTTPRETTY_DEPENDENCIES:= nose sure
export PYTHONPATH:= ${PWD}

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@for dependency in `echo $$HTTPRETTY_DEPENDENCIES`; do \
		python -c "import $$dependency" 2>/dev/null || (echo "You must install $$dependency in order to run httpretty's tests" && exit 3) ; \
		done

test: unit functional acceptance

lint:
	@echo "Checking code style ..."
	@flake8 httpretty

unit: prepare lint
	@echo "Running unit tests ..."
	@nosetests --rednose -x --with-randomly --with-coverage --cover-package=httpretty -s tests/unit

functional: prepare
	@echo "Running functional tests ..."
	@nosetests --rednose -x --with-randomly --with-coverage --cover-package=httpretty -s tests/functional

acceptance: prepare
	@echo "Running documentation tests tests ..."
	@steadymark README.md

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; done
	@echo "OK!"

release: clean unit functional
	@echo "Releasing httpretty..."
	@./.release
	@python setup.py sdist bdist_wheel register upload

docs: acceptance
	@cd docs && make html
	$(OPEN_COMMAND) docs/build/html/index.html

deploy-docs:
	@git co master && \
		(git br -D gh-pages || printf "") && \
		git checkout --orphan gh-pages && \
		markment -o . -t ./theme --sitemap-for="http://falcao.it/HTTPretty" docs && \
		git add . && \
		git commit -am 'documentation' && \
		git push --force origin gh-pages && \
		git checkout master

prepare:
	@reset


.PHONY: docs
