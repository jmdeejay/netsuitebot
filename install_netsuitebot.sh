#!/bin/bash

set -e;

# Get source real dir: Upstreams symlinks.
SOURCE="${BASH_SOURCE[0]}";
while [ -h "$SOURCE" ]; do
    DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)";
    SOURCE="$(readlink "$SOURCE")";
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE";
done
DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)";

# Consts
readonly RED='\033[0;31m';
readonly BLUE='\033[0;34m';
readonly NC='\033[0m';
readonly APP_NAME="NetsuiteBot";
readonly COLORED_APP_NAME="${BLUE}Netsuite${NC}${RED}Bot${NC}";
readonly CUR_DIR="$DIR";
readonly BASE_PATH="$HOME/netsuitebot";
readonly CONFIGURATOR_FILENAME="Configurator.appimage";
readonly BOT_FILENAME="NetsuiteBot";

printHelp () {
  echo -e "This script will install $COLORED_APP_NAME and its cron.

Options
  -h | --help Show you this help.
  -r | --remove Uninstall $APP_NAME and its cron.
  -u | --update Update $APP_NAME.";
}

netsuitebot_is_compiled () {
    [[ -f "$CUR_DIR/dist/$CONFIGURATOR_FILENAME" && -f "$CUR_DIR/dist/$BOT_FILENAME" ]];
}

netsuitebot_is_installed () {
    [[ -f "$BASE_PATH/$CONFIGURATOR_FILENAME" && -f "$BASE_PATH/$BOT_FILENAME" ]];
}

install () {
  if netsuitebot_is_installed; then
    echo "$APP_NAME is already installed";
  else
    if netsuitebot_is_compiled; then
      mkdir -p "$BASE_PATH/";
      cp "$CUR_DIR/dist/$CONFIGURATOR_FILENAME" "$BASE_PATH/$CONFIGURATOR_FILENAME";
      cp "$CUR_DIR/dist/$BOT_FILENAME" "$BASE_PATH/$BOT_FILENAME";
      echo "$APP_NAME successfully installed";
      # Install cronjob
      pipenv run python "$CUR_DIR/src/cron.py" "install" "$BASE_PATH" "$BOT_FILENAME";
      # Execute Configurator
      cd "$BASE_PATH" && ./$CONFIGURATOR_FILENAME &> /dev/null &
    else
      echo -e "${RED}[Error]${NC}: Compiled applications missing."
      echo "Run \`make compile_applications\` before trying to install."
    fi
  fi
}

uninstall () {
  if ! netsuitebot_is_installed; then
    echo "$APP_NAME is already uninstalled";
  else
    # Uninstall cronjob
    pipenv run python "$CUR_DIR/src/cron.py" "uninstall" "$BASE_PATH" "$BOT_FILENAME";
    rm -f "$BASE_PATH/$CONFIGURATOR_FILENAME";
    rm -f "$BASE_PATH/$BOT_FILENAME";
    rm -f "$BASE_PATH/configs.ini";
    rm -f "$BASE_PATH/cron.log";
    echo "$APP_NAME uninstalled";
  fi
}

update () {
  if netsuitebot_is_installed; then
    cd "$CUR_DIR" || echo "Error when updating.";
    git pull --ff-only;
	  make configurator;
    make netsuitebot;
    cp "$CUR_DIR/dist/$CONFIGURATOR_FILENAME" "$BASE_PATH/$CONFIGURATOR_FILENAME";
    cp "$CUR_DIR/dist/$BOT_FILENAME" "$BASE_PATH/$BOT_FILENAME";
    echo "$APP_NAME successfully updated";
  else
    echo "$APP_NAME does not seem to be installed. Install it before updating.";
  fi
}

if [[ $1 == "-h" || $1 == "--help" ]]; then # Help
  printHelp;
elif [[ -z "$1" ]]; then #Install
  install;
elif [[ $1 == "-r" || $1 == "--remove" ]]; then # Uninstall
  uninstall;
elif [[ $1 == "-u" || $1 == "--update" ]]; then # Update
  update;
else
  printHelp;
fi
