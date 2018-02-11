test:
	python -t -m embypy
upload:
	python3 setup.py sdist upload
docs:
	$(MAKE) -C docs/ rst
