#!/bin/bash
# Setup script for reproducing the project environment

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete! Virtual environment ready."
echo "To activate in future sessions, run: source venv/bin/activate"
