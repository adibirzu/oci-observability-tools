.PHONY: check test build linkcheck

check:
	python -m ruff check .
	python -m pytest -q
	python scripts/redaction_check.py .

test:
	python -m pytest -q

build:
	python scripts/gen_oracle_docs.py --check
	python scripts/build_chatgpt.py --check

linkcheck:
	@echo "Manual online task: verify catalog URLs return HTTP 200"
