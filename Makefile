resolve:
	pip install -r requirements.txt
check:
	flake8 tosspay/
test:
	py.test tests/
