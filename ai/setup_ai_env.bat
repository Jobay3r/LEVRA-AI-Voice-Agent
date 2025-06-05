@echo off
echo Setting up AI environment...
echo.

REM Create virtual environment if it doesn't exist
if not exist "Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .
)

REM Activate virtual environment and install requirements
echo Activating virtual environment and installing packages...
call Scripts\activate.bat
pip install -r requirements.txt

echo.
echo AI environment setup complete!
echo To activate: cd ai && Scripts\activate.bat
pause
