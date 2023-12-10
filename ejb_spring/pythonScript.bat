@echo hello
set BACKEND_BASE_URL=https://genai-preprod-3446x4g1.wl.gateway.dev
set API_GATEWAY_KEY=AIzaSyALBWXIFLYT-ZmIwVyO9vpeQ201KymJk00
REM Replace 'path_to_venv' with the actual path to your virtual environment's activate script.
set "script_dir=%~dp0"

call "%script_dir%venv\Scripts\activate"

python "%script_dir%server\ejb_spring_boot\manage.py" %1 %2 %3

REM Deactivate the virtual environment.
call "%script_dir%venv\Scripts\deactivate"