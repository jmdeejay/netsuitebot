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
readonly BASE_PATH="$DIR";
readonly CONFIGURATOR_FILENAME="configurator.py";
readonly BOT_FILENAME="netsuitebot.py";

printHelp () {
  echo -e "This script will install $COLORED_APP_NAME and its cron.

Options
  -h | --help Show you this help.
  -r | --remove Uninstall $APP_NAME and its cron.
  -u | --update Update $APP_NAME.";
}

install () {
  # Install cronjob
  pipenv run python "$BASE_PATH/src/cron.py" "install" "$BASE_PATH/src/" "$BOT_FILENAME";
  echo "$APP_NAME successfully installed";
  # Execute Configurator
  cd "$BASE_PATH" && pipenv run python ./src/$CONFIGURATOR_FILENAME &> /dev/null &
}

uninstall () {
  # Uninstall cronjob
  pipenv run python "$BASE_PATH/src/cron.py" "uninstall" "$BASE_PATH/src/" "$BOT_FILENAME";
  rm -f "$BASE_PATH/configs.ini";
  rm -f "$BASE_PATH/cron.log";
  echo "$APP_NAME uninstalled";
}

update () {
  cd "$BASE_PATH" || echo "Error when updating.";
  git pull --ff-only;
  echo "$APP_NAME successfully updated";
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
