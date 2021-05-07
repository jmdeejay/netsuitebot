SHELL := /bin/bash

# Setup
.PHONY: install_requirements
CHECK_PLUGIN_LIST = $(shell asdf plugin list | grep "python")
GET_PLUGIN_LIST = $(eval LIST_CONTENT=$(CHECK_PLUGIN_LIST))
install_requirements:
	$(GET_PLUGIN_LIST)
	@if [[ $(LIST_CONTENT) == "python" ]]; then \
  		asdf plugin update python; \
  	else \
		asdf plugin add python; \
	fi
	@asdf install
	@pip install --upgrade pip
	@pip install pipenv
	@pipenv --python 3.8.3
	@pipenv install

# User installation
.PHONY: install_netsuitebot
install_netsuitebot:
	./install_netsuitebot.sh

.PHONY: uninstall_netsuitebot
uninstall_netsuitebot:
	./install_netsuitebot.sh --remove

.PHONY: update_netsuitebot
update_netsuitebot:
	./install_netsuitebot.sh --update

# Dev installation
.PHONY: install_dev_requirements
install_dev_requirements:
	pipenv install --dev

# Linting code style & stats
.PHONY: code_style
code_style:
	pipenv run pycodestyle --statistics --count

.PHONY: code_lint
code_lint:
	pipenv run flake8

.PHONY: count_lines
count_lines:
	line -d
