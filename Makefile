init:
	pip install -r requirements.txt

test:
	py.test --pyargs nbd

release:
	python scripts/pypi_upload.py

.PHONY: init test
