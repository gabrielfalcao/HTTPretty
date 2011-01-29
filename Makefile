all: check_dependencies unit functional integration doctest

filename=httpretty-`python -c 'import httpretty;print httpretty.version'`.tar.gz

#export PYTHONPATH:= ${PWD}
export HTTPRETTY_DEPENDENCIES:= nose sure

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@for dependency in `echo $$HTTPRETTY_DEPENDENCIES`; do \
		python -c "import $$dependency" 2>/dev/null || (echo "You must install $$dependency in order to run httpretty's tests" && exit 3) ; \
		done

unit: clean
	@echo "Running unit tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/unit --cover-package=httpretty

functional: clean
	@echo "Running functional tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/functional --cover-package=httpretty

integration: clean
	@echo "Running integration tests ..."
	@nosetests -s --verbosity=2 tests/integration

doctest: clean
	@cd docs && make doctest

documentation:
	@cd docs && make html

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; done
	@echo "OK!"

release: clean unit functional integration doctest deploy-documentation
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) httpretty setup.py README.md COPYING
	@echo "DONE!"
