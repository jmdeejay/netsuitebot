#!/bin/bash

if ! command -v asdf &>/dev/null; then
  echo "[Error] Make sure asdf is installed before trying to run the initial setup."
  exit
fi

LIST_CONTENT=$(asdf plugin list | grep "python")
if [[ "$(uname)" == 'Darwin' ]]; then
  echo "Installing xcode-select..."
  echo "If xcode-select is already installed, it will output an error."
  echo "Don't worry, the script will continue."
  xcode-select --install

  echo "Updating Brew..."
  echo "Please be patient. It can take a reaaaaaally long time."
  brew update

  echo "Installing global dependencies..."
  brew install make wget curl python-tk

  echo "Installing Python with asdf..."
  if [[ "$LIST_CONTENT" == "python" ]]; then
    asdf plugin update python
  else
    asdf plugin add python
  fi
  env PATH="$(brew --prefix tcl-tk)/bin:$PATH" LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
    CPPFLAGS="-I$(brew --prefix tcl-tk)/include" PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
    CFLAGS="-I$(brew --prefix tcl-tk)/include" \
    PYTHON_CONFIGURE_OPTS="--enable-framework --with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
    asdf install
  asdf reshim

  echo "Installing pip..."
  pip install --upgrade pip

  echo "Installing pipenv..."
  sudo pip install pipenv

  echo "Starting pipenv environment..."
  pipenv --python 3.8.3

  echo "Installing python dependencies..."
  pipenv install
elif [[ "$(uname)" == 'Linux' ]]; then
  echo "Installing global dependencies..."
  sudo apt-get install --no-install-recommends make build-essential wget curl tk-dev python-tk python3-tk

  echo "Installing Python with asdf..."
  if [[ "$LIST_CONTENT" == "python" ]]; then
    asdf plugin update python
  else
    asdf plugin add python
  fi
  env PYTHON_CONFIGURE_OPTS="--enable-shared" asdf install

  echo "Installing pip..."
  pip install --upgrade pip

  echo "Installing pipenv..."
  pip install pipenv

  echo "Starting pipenv environment..."
  pipenv --python 3.8.3

  echo "Installing python dependencies..."
  pipenv install
fi
