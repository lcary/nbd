init:
	pip install -r requirements.txt

test:
	py.test --pyargs nbd

.PHONY: init test
