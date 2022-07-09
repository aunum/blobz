
.PHONY: test
test:
	python -m pytest -vv ./tests -s --log-cli-level=INFO

.PHONY: dist
dist:
	python -m build
	twine upload dist/*