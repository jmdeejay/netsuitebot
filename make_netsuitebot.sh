#!/bin/bash

# shellcheck disable=SC2164
cd "$(pwd)" || echo "Error changing path.";

# Create NetsuiteBot executable
AppName="NetsuiteBot";
fileName="netsuitebot";

# --clean to clear cache
pyinstaller --onefile "./src/$fileName.py" --noconfirm --name "$AppName" \
            --paths './src/' \
            --specpath "./build/$AppName/$fileName.spec";
