
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
	python setup.py clean
	cd src && make clean

dist: clean
	python setup.py bdist_wheel
	python setup.py sdist

docs: install-dev
	cd docs && make html

install-dev:
	pip install --quiet -r requirements-dev.txt

install: install-dev
	pip install --quiet -r requirements.txt
	python setup.py install
