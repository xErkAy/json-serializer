fmt:
	ruff format
	toml-sort pyproject.toml


check:
	ruff check --fix --unsafe-fixes
	mypy ./


lint:
	make fmt
	make check