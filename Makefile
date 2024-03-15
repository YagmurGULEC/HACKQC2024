SHELL=./make-venv
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1
all: help

.PHONY: help
help: Makefile
	@echo "Choose a command run:"
	@(sed -n "s/^## //p" Makefile | column -t -s ":" | sed -e "s/^/  /")

## install: installs dependencies under venv
.PHONY: install
install:
	python3.9 -m venv ~/.venv
	pip install --upgrade pip
	make post-install

.PHONY: post-install
post-install:
	pip install -r requirements.txt
run:
	python main.py
