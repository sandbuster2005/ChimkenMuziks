#!/bin/bash
if [ -d ".env" ]; then
   source .env/bin/activate
   python lecteur.py "$1" "$2" 

else
   python -m venv .env
   source .env/bin/activate
   pip install -r requirement
   python lecteur.py "$1" "$2"
fi
