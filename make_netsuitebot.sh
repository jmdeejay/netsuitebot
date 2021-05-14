#!/bin/bash

# shellcheck disable=SC2164
cd "$(pwd)" || echo "Error changing path."

# Create NetsuiteBot executable
AppName="NetsuiteBot"
fileName="netsuitebot"

# --clean to clear cache
pipenv run pyinstaller --onefile "./src/$fileName.py" --noconfirm --noupx --name "$AppName" \
  --icon '../../../resources/netsuitebot_logo.icns' \
  --paths './src/' \
  --specpath "./build/$AppName/$fileName.spec"
