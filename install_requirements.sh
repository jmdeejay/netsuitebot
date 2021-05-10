#!/bin/bash

if ! command -v asdf &> /dev/null; then
    echo "[Error] Make sure asdf is installed before trying to run the initial setup.";
    exit;
fi

LIST_CONTENT=$(asdf plugin list | grep "python");
if [[ "$(uname)" == 'Darwin' ]]; then
  xcode-select --install;
	brew update;
	brew install make wget curl python-tk;
	if [[ "$LIST_CONTENT" == "python" ]]; then
	  asdf plugin update python;
  else
		asdf plugin add python;
	fi
	env PATH="$(brew --prefix tcl-tk)/bin:$PATH" LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
	CPPFLAGS="-I$(brew --prefix tcl-tk)/include" PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
	CFLAGS="-I$(brew --prefix tcl-tk)/include" \
	PYTHON_CONFIGURE_OPTS="--enable-framework --with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
	asdf install;
	asdf reshim;
	pip install --upgrade pip;
	pip install pipenv;
	pipenv --python 3.8.3;
	pipenv install;
else
  sudo apt-get install --no-install-recommends make build-essential wget curl tk-dev python-tk python3-tk;
	if [[ "$LIST_CONTENT" == "python" ]]; then
	  asdf plugin update python;
	else
		asdf plugin add python;
	fi
	env PYTHON_CONFIGURE_OPTS="--enable-shared" asdf install;
	pip install --upgrade pip;
	pip install pipenv;
	pipenv --python 3.8.3;
	pipenv install;
fi
