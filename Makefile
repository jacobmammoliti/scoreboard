.ONESHELL:

all: install test run

install: venv
	. venv/bin/activate && pip install -r requirements.txt

venv:
	test -d venv || python3 -m venv venv
	
run:
	. venv/bin/activate && python src/main.py

test:
	. venv/bin/activate && cd src && python -m unittest tests.py

clean:
	rm -rf venv