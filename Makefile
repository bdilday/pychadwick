
.PHONY : clean


lint: install-dev
	python -m black pychadwick/ tests/
	python -m flake8 pychadwick


test: install
	pytest tests/

clean:
	rm -fr pychadwick.egg-info
	rm -fr build
	rm -fr dist
	rm -rf _skbuild
	python setup.py clean

dist: clean
	python setup.py bdist_wheel
	python setup.py sdist

docs: install-dev
	cd docs && make html

install-dev:
	pip install --quiet -r requirements-dev.txt

install: clean
	pip install --quiet -r requirements-dev.txt
	pip install --quiet -r requirements.txt
	python setup.py install
