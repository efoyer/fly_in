FNAME = fly_in.py
ARG ?=
MODULES = flake8 mypy

run:
	python3 $(FNAME) $(ARG)

install:
	pip install $(MODULES)

debug:
	python3 -m pdb $(FNAME) $(ARG)

clean:
	rm -rf __pycache__ .mypy_cache *.pyc src/__pycache__

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict