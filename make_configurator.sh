#!/bin/bash

# shellcheck disable=SC2164
cd "$(pwd)" || echo "Error changing path.";

# Create Configurator executable
AppName="Configurator";
fileName="configurator";

# Copy logo data to pack
imageFileName="netsuite_logo.png";
imageFilepath="./build/$AppName/$fileName.spec/";
mkdir -p "$imageFilepath";
cp "./src/$imageFileName" "$imageFilepath";

# --clean to clear cache
pipenv run pyinstaller --onefile "./src/$fileName.py" --noconfirm --noupx --name "$AppName" \
            --paths "./src/" \
            --hidden-import="PIL._tkinter_finder" \
            --add-data "$imageFileName:./src/" \
            --specpath "./build/$AppName/$fileName.spec";

mv "./dist/$AppName" "./dist/$AppName.appimage";
