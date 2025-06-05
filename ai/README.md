# AI Environment Setup

This folder contains the Python virtual environment and dependencies for the AI components of LEVRA.

## Setup Instructions

### Windows (Batch)

```cmd
setup_ai_env.bat
```

### Windows (PowerShell)

```powershell
.\setup_ai_env.ps1
```

### Manual Setup

```cmd
# Create virtual environment
python -m venv .

# Activate virtual environment
Scripts\activate.bat  # Windows CMD
# OR
Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

## Usage

After setup, activate the environment before running AI-related scripts:

```cmd
# Navigate to ai folder
cd ai

# Activate environment
Scripts\activate.bat  # Windows CMD
# OR
Scripts\Activate.ps1  # Windows PowerShell

# Your environment is now ready for AI development
```

## Dependencies

All Python dependencies are listed in `requirements.txt`. The virtual environment folders (`Lib/`, `Scripts/`, etc.) are excluded from version control to keep the repository clean.
