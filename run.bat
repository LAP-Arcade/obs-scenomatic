if not exist venv\Scripts\python.exe (
    python -m venv venv
    venv\Scripts\pip install -r requirements.txt
)
venv\Scripts\python main.py %*
