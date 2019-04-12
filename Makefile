all: venv

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

venv:
	virtualenv --python=python3 venv && pip install -r requirements.txt

requirements:
	pip install -r requirements.txt

.PHONY: clean venv
