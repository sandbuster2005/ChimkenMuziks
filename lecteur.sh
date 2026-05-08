#!/bin/bash
if [ -d ".env" ]; then
   source .env/bin/activate
   if [ $1 ]; then
   python lecteur.py "$1" "$2" 
   
   else
   python lecteur.py
   fi

else
   python -m venv .env
   source .env/bin/activate
   pip install -r requirement
   if [ $1 ]; then
   python lecteur.py "$1" "$2" 
   
   else
   python lecteur.py
   fi
fi
