#!/bin/bash

# Get the clicked path argument passed by Visual Studio Code
#clickedPath=$1

#path="/Users/yogeshsharma8/Documents/Hashedin/acme-ejb-project/.vscode"
#cleanPath=$(dirname "$path")
#echo "$cleanPath"

cleanPath=$(dirname "$clickedPath")
echo "$cleanPath"

# Additional parameters
param1=$2
#param2=$3
currentScriptDir=$(dirname "$0")
param2=$(/usr/local/bin/python3 /Users/yogeshsharma8/Documents/Hashedin/genai_migration/ejb_spring/file_picker.py)
#param2=$(zenity --file-selection --title="Select a File")

# Run your .sh script (init.sh) with the clicked path and additional parameters
bash "$currentScriptDir/pythonScript.sh" "$cleanPath" "$param1" "$param2"