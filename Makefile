all: check_dependencies unit functional doctests

filename=httpretty-`python -c 'import httpretty;print httpretty.version'`.tar.gz

export HTTPRETTY_DEPENDENCIES:= nose sure
export PYTHONPATH:= ${PWD}

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@for dependency in `echo $$HTTPRETTY_DEPENDENCIES`; do \
		python -c "import $$dependency" 2>/dev/null || (echo "You must install $$dependency in order to run httpretty's tests" && exit 3) ; \
		done

test: unit functional doctests

unit: prepare
	@echo "Running unit tests ..."
	@nosetests --stop -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/unit --cover-package=httpretty

functional: prepare
	@echo "Running functional tests ..."
	@nosetests --stop -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/functional --cover-package=httpretty

doctests: prepare
	@echo "Running documentation tests tests ..."
	@steadymark README.md

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; done
	@echo "OK!"

release: clean unit functional
	@echo "Releasing httpretty..."
	@./.release
	@python setup.py sdist register upload

docs: doctests
	@markment -o . -t ./theme --sitemap-for="http://falcao.it/HTTPretty" docs

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
