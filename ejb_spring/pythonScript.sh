#!/bin/bash
export  BACKEND_BASE_URL=https://genai-preprod-3446x4g1.wl.gateway.dev
export  API_GATEWAY_KEY=AIzaSyALBWXIFLYT-ZmIwVyO9vpeQ201KymJk00
# Replace 'path_to_venv' with the actual path to your virtual environment's activate script.
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $script_dir/venv/bin/activate

python3 $script_dir/server/ejb_spring_boot/manage.py "$1" "$2" "$3"

# Deactivate the virtual environment.
deactivate