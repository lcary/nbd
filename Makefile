init:
	pip install -r requirements.txt

test:
	py.test --pyargs nbd

install:
	python scripts/test_install.py

release:
	python scripts/pypi_upload.py

.PHONY: init test install release
