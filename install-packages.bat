@echo off

:: Check if tqdm is installed
python -c "import tqdm" 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo tqdm not found. Installing tqdm...
    python -m pip install tqdm
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install tqdm. Please install it manually.
        exit /b 1
    )
)