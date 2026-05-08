if exist .env\ (
   if exist .env\bin\ (
      .env\bin\activate.bat
   ) else (
      .env\Scripts\activate.bat
   )
   python lecteur.py
) else (
   python -m venv .env
   .env\Scripts\activate.bat
   pip install -r requirement
   python lecteur.py
)