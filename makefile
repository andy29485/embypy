test:
	python -t -m embypy
upload:
	python3 setup.py sdist
	twine upload dist/* --username Andy29485

docs:
	$(MAKE) -C docs/ rst
