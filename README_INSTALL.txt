INSTALLAZIONE RAPIDA WINDOWS POWERSHELL
1) Estrarre il contenuto nella root del progetto, senza sovrascrivere .venv.
2) Attivare: .\.venv\Scripts\Activate.ps1
3) Installare: python -m pip install -r requirements.txt
4) Copiare: Copy-Item .env.example .env
5) Avviare: python -m streamlit run app.py
Timestral e opzionale: installare con requirements-timestral.txt e impostare TIMESTRAL_ENABLED=true.
