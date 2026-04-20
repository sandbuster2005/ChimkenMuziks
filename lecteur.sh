#!/bin/bash

if [ -d ".env" ]; then
   source .env/bin/activate
   python lecteur.py

else
   python -m venv .env
   source .env/bin/activate
   pip install -r requirement
   python lecteur.py
fi
