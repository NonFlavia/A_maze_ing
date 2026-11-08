install:
	python3 -m pip install flake8 mypy build

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache
	rm -rf build dist *.egg-info *.whl

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict

build:
	python3 -m build --wheel --outdir .
