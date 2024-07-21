#!/bin/bash

echo "Current directory: $(pwd)"
echo "Contents of current directory:"
ls -la

echo "Contents of ${APP_HOME} directory:"
ls -la ${APP_HOME}/

echo "Python version:"
python --version

echo "PYTHONPATH: $PYTHONPATH"

echo "Trying to import app module:"
python -c "import app; print(app.__file__)"

echo "Starting uvicorn:"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload