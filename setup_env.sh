#!/bin/bash

# Create virtual environment
python3 -m venv project_env
source myenv/bin/activate

# Install dependencies for code style, gui support etc.
sudo apt install python3-pycodestyle python3-pydocstyle python3-opengl python3-wxgtk4.0 freeglut3-dev

# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Virtual environment created, dependencies installed, and necessary packages installed successfully."

