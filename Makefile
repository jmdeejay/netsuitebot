SHELL := /bin/bash

# Initial setup
.PHONY: install_requirements
CHECK_PLUGIN_LIST = $(shell asdf plugin list | grep "python")
GET_PLUGIN_LIST = $(eval LIST_CONTENT=$(CHECK_PLUGIN_LIST))
install_requirements:
	@if [[ "$(uname)" == 'Darwin' ]]; then \
		xcode-select --install \
		brew update \
		brew install make wget curl python-tk; \
		$(GET_PLUGIN_LIST) \
		@if [[ "$(LIST_CONTENT)" == "python" ]]; then \
  			asdf plugin update python; \
  		else \
			asdf plugin add python; \
		fi \
		@env \
		PATH="$(brew --prefix tcl-tk)/bin:$PATH" \
		LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
		CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \
		PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
		CFLAGS="-I$(brew --prefix tcl-tk)/include" \
		PYTHON_CONFIGURE_OPTS="--enable-framework --with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
		asdf install \
		@asdf reshim \
		@pip install --upgrade pip \
		@pip install pipenv \
		@pipenv --python 3.8.3 \
		@pipenv install \
    else \
		sudo apt-get install --no-install-recommends make build-essential wget curl tk-dev python-tk python3-tk; \
		$(GET_PLUGIN_LIST) \
		@if [[ "$(LIST_CONTENT)" == "python" ]]; then \
			  asdf plugin update python; \
		else \
			asdf plugin add python; \
		fi \
		@env PYTHON_CONFIGURE_OPTS="--enable-shared" asdf install \
		@asdf reshim \
		@pip install --upgrade pip \
		@pip install pipenv \
		@pipenv --python 3.8.3 \
		@pipenv install \
    fi


# Compile project applications
.PHONY: compile_applications
compile_applications: configurator netsuitebot

.PHONY: configurator
configurator:
	./make_configurator.sh

.PHONY: netsuitebot
netsuitebot:
	./make_netsuitebot.sh


# Application installation
.PHONY: install_netsuitebot
install_netsuitebot:
	./install_netsuitebot.sh

.PHONY: uninstall_netsuitebot
uninstall_netsuitebot:
	./install_netsuitebot.sh --remove

.PHONY: update_netsuitebot
update_netsuitebot:
	./install_netsuitebot.sh --update


# Dev requireemnts installation
.PHONY: install_dev_requirements
install_dev_requirements:
	pipenv install --dev


# Linting, code style, type check & stats
.PHONY: code_style
code_style:
	pipenv run pycodestyle --statistics --count

.PHONY: code_lint
code_lint:
	pipenv run flake8

.PHONY: type_check
type_check:
	pipenv run pytype -d import-error

.PHONY: count_lines
count_lines:
	line -d
