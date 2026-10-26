# HR Future Insights

**AI-powered Workforce Forecasting & Decision Intelligence**

HR Future Insights e una web application locale progettata per dimostrare le potenzialita dell'AI applicata ai processi HR e SAP HCM. La soluzione combina:

- **Timestral** per il forecasting probabilistico delle serie temporali HR;
- **Ollama** per query in linguaggio naturale e insight executive;
- **Streamlit** per la dashboard interattiva;
- **Plotly** per grafici e intervalli di confidenza;
- **SQLite** per memoria della chat, sessioni e scenari;
- dati HR **sintetici**, senza collegamento a SAP nella fase PoC.

> **Stato del progetto:** Proof of Concept locale. I valori visualizzati sono sintetici e non devono essere utilizzati per decisioni HR reali. Prima di un uso enterprise sono necessari backtesting, sicurezza, governance, autorizzazioni e validazione legale/licensing.

---

## 1. Funzionalita principali

- Dashboard executive con KPI di **Headcount, Assenze, Turnover e Payroll**.
- Forecast storici e futuri con **intervalli probabilistici**.
- Scenario Simulator per nuove assunzioni, aumenti salariali, smart working e retention.
- HR AI Assistant con query in italiano tramite modelli locali Ollama.
- Selezione dinamica dei modelli Ollama installati sul PC.
- Memoria della conversazione e persistenza delle sessioni in SQLite.
- Generazione di insight executive basati su KPI e scenari attivi.
- Funzionamento locale senza invio volontario dei dati HR a servizi cloud.

---

## 2. Architettura logica

```text
Browser locale
      |
      v
Streamlit Web App
      |
      +----------------------+----------------------+
      |                      |                      |
      v                      v                      v
Forecast Service       Ollama Service        Memory Service
Timestral              LLM locale            SQLite
      |                      |                      |
      +----------------------+----------------------+
                             |
                             v
                     Dati HR sintetici
```

### Separazione delle responsabilita

- **Timestral** prevede valori numerici futuri e quantili di incertezza.
- **Ollama** interpreta domande, seleziona l'intento e formula risposte manageriali.
- **Streamlit** gestisce interfaccia, navigazione, grafici e session state.
- **SQLite** conserva conversazioni, scenari, configurazioni e storico dei forecast.

---

## 3. Requisiti del PC Surface con Windows 11

### Requisiti minimi per la demo

- Windows 11 aggiornato.
- CPU Intel, AMD oppure Qualcomm Snapdragon/ARM64.
- **16 GB di RAM consigliati**; con 8 GB usare modelli Ollama molto piccoli.
- Almeno **15 GB liberi** per ambiente Python, Timestral e uno o due modelli Ollama.
- Connessione Internet necessaria solo per installazione e download iniziale dei modelli.
- Browser recente: Microsoft Edge o Google Chrome.

### Configurazione consigliata

- **16 GB RAM:** Timestral-28M + LLM Ollama da 3B/4B parametri.
- **32 GB RAM:** Timestral-123M o 209M + LLM Ollama da 7B/8B parametri.
- Surface senza GPU dedicata: utilizzare CPU e modelli quantizzati piccoli.
- Surface ARM64: installare Python ARM64 e verificare la disponibilita delle build PyTorch per la versione scelta.

> La memoria effettiva dipende dalla quantizzazione del modello Ollama, dalla lunghezza del contesto e dal numero di processi aperti. Chiudere applicazioni pesanti durante la demo.

---

## 4. Software richiesto

### Obbligatorio

1. **Python 3.12, 64 bit**, raccomandato per stabilita e compatibilita del PoC.
2. **Git for Windows**, necessario per installare Timestral dal repository ufficiale.
3. **Ollama for Windows**, per i modelli linguistici locali.
4. Il progetto HR Future Insights estratto in una cartella locale.

### Facoltativo

- Visual Studio Code con estensione Python.
- Docker Desktop, solo se si vuole utilizzare il packaging containerizzato.
- Windows Terminal per una migliore esperienza PowerShell.

---

## 5. Verifica dell'architettura del Surface

Aprire **PowerShell** e lanciare:

```powershell
$env:PROCESSOR_ARCHITECTURE
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, TotalPhysicalMemory
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
```

Valori comuni:

- `AMD64`: Surface con processore Intel o AMD, utilizzare installer Python x64.
- `ARM64`: Surface con processore Snapdragon, utilizzare installer Python ARM64.

---

## 6. Installazione di Python

Scaricare Python dal sito ufficiale:

- https://www.python.org/downloads/windows/

Per questo PoC e consigliato **Python 3.12.x**. Durante l'installazione tradizionale:

1. Selezionare **Add python.exe to PATH**.
2. Selezionare **pip** e **venv**.
3. Completare l'installazione.
4. Chiudere e riaprire PowerShell.

Verificare:

```powershell
python --version
python -m pip --version
```

Output atteso:

```text
Python 3.12.x
pip 2x.x from ...
```

Se il comando `python` apre Microsoft Store oppure non viene trovato:

```powershell
py --version
```

Nei comandi successivi e possibile sostituire `python` con `py -3.12`.

---

## 7. Installazione di Git for Windows

Scaricare Git:

- https://git-scm.com/download/win

Installare mantenendo le opzioni predefinite, quindi verificare:

```powershell
git --version
```

Git e richiesto per il comando:

```powershell
pip install git+https://github.com/mistralai/timestral.git
```

---

## 8. Installazione di Ollama su Windows 11

Pagina ufficiale:

- https://ollama.com/download/windows

In alternativa, da PowerShell:

```powershell
irm https://ollama.com/install.ps1 | iex
```

Dopo l'installazione, aprire una nuova finestra PowerShell e verificare:

```powershell
ollama --version
```

Ollama viene eseguito in background e rende disponibile l'API locale su:

```text
http://localhost:11434
```

Test dell'API:

```powershell
Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get
```

### Modello consigliato per iniziare

Per un Surface con 16 GB RAM utilizzare un modello piccolo disponibile nella libreria Ollama, ad esempio:

```powershell
ollama pull qwen3:4b
```

Se il PC ha meno memoria, scegliere una variante ancora piu piccola. Per elencare i modelli installati:

```powershell
ollama list
```

Per effettuare un test interattivo:

```powershell
ollama run qwen3:4b
```

Per uscire:

```text
/bye
```

> La webapp non usa un nome modello codificato: interroga `/api/tags` e permette all'utente di selezionare uno dei modelli installati.

---

## 9. Posizionamento del progetto

Estrarre il progetto in una cartella locale senza spazi eccessivi nel percorso, per esempio:

```text
C:\Projects\hr-future-insights
```

Aprire PowerShell nella cartella:

```powershell
cd C:\Projects\hr-future-insights
```

La struttura attesa e simile alla seguente:

```text
hr-future-insights/
|-- app.py
|-- requirements.txt
|-- .env.example
|-- README.md
|-- assets/
|   `-- style.css
|-- config/
|   `-- settings.py
|-- data/
|   `-- synthetic_generator.py
|-- pages/
|   |-- 1_Dashboard.py
|   |-- 2_Forecasting.py
|   |-- 3_AI_Chat.py
|   |-- 4_Scenarios.py
|   `-- 5_Reports.py
|-- services/
|   |-- forecasting_service.py
|   |-- timestral_service.py
|   |-- ollama_service.py
|   |-- memory_service.py
|   |-- insight_service.py
|   `-- database_service.py
|-- database/
|   `-- schema.sql
|-- storage/
|-- tests/
|-- Dockerfile
`-- docker-compose.yml
```

> I nomi possono differire leggermente in base alla release. Il punto di ingresso predefinito rimane `app.py`.

---

## 10. Creazione dell'ambiente virtuale

Dalla root del progetto:

```powershell
python -m venv .venv
```

Attivazione in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Il prompt dovrebbe iniziare con:

```text
(.venv) PS C:\Projects\hr-future-insights>
```

### Errore ExecutionPolicy

Se PowerShell blocca `Activate.ps1`, eseguire soltanto per la sessione corrente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Non e necessario modificare la policy globale del PC.

Aggiornare gli strumenti di packaging:

```powershell
python -m pip install --upgrade pip setuptools wheel
```

---

## 11. Installazione delle dipendenze Python

Installare le dipendenze applicative:

```powershell
pip install -r requirements.txt
```

Il file `requirements.txt` dovrebbe includere almeno:

```text
streamlit
plotly
pandas
numpy
requests
python-dotenv
pydantic
sqlalchemy
```

Se il progetto utilizza direttamente Timestral, installare anche PyTorch e Timestral:

```powershell
pip install "torch>=2.4"
pip install git+https://github.com/mistralai/timestral.git
```

Verificare:

```powershell
python -c "import streamlit, pandas, plotly, torch; print('Dipendenze base OK')"
python -c "from timestral import TimestralForecaster; print('Timestral OK')"
```

### Installazione CPU esplicita di PyTorch

Se `pip install torch` presenta problemi o installa componenti non adatti, usare il selettore ufficiale PyTorch:

- https://pytorch.org/get-started/locally/

Su un Surface senza GPU NVIDIA, scegliere Windows, Pip, Python e CPU.

---

## 12. Modello Timestral consigliato

Timestral e disponibile nelle dimensioni 5M, 28M, 123M e 209M. Per una demo su Surface:

- `mistralai/Timestral-5M`: test rapido e footprint minimo;
- `mistralai/Timestral-28M`: configurazione raccomandata per il PoC;
- `mistralai/Timestral-123M`: qualita superiore, maggiore RAM e latenza;
- `mistralai/Timestral-209M`: modello piu grande, da usare solo dopo test sul PC.

Configurazione suggerita:

```text
TIMESTRAL_MODEL=mistralai/Timestral-28M
TIMESTRAL_DEVICE=cpu
```

Al primo avvio i pesi vengono scaricati da Hugging Face e poi mantenuti nella cache locale. Il download iniziale richiede connessione Internet.

---

## 13. Configurazione del file `.env`

Se presente, copiare il template:

```powershell
Copy-Item .env.example .env
```

Se `.env.example` non esiste, creare `.env` nella root del progetto con:

```dotenv
APP_NAME=HR Future Insights
APP_ENV=development
APP_HOST=localhost
APP_PORT=8501

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_REQUEST_TIMEOUT=180
OLLAMA_DEFAULT_MODEL=qwen3:4b

TIMESTRAL_ENABLED=true
TIMESTRAL_MODEL=mistralai/Timestral-28M
TIMESTRAL_DEVICE=cpu
TIMESTRAL_FORECAST_HORIZON=12

DATABASE_URL=sqlite:///storage/hr_future_insights.db
CHAT_MEMORY_MAX_MESSAGES=20
CHAT_SUMMARY_THRESHOLD=20

USE_SYNTHETIC_DATA=true
SYNTHETIC_DATA_SEED=42
LOG_LEVEL=INFO
```

### Note di sicurezza

- Non inserire password SAP, token o dati personali reali nel file `.env`.
- Il file `.env` deve essere incluso in `.gitignore`.
- Nel PoC usare esclusivamente dati sintetici o autorizzati.

---

## 14. Avvio rapido

Assicurarsi che Ollama sia attivo:

```powershell
ollama list
```

Dalla root del progetto, con `.venv` attivo:

```powershell
python -m streamlit run app.py
```

La webapp dovrebbe aprirsi automaticamente nel browser. In alternativa:

```text
http://localhost:8501
```

Se la porta 8501 e occupata:

```powershell
python -m streamlit run app.py --server.port 8502
```

---

## 15. Procedura demo consigliata

1. Aprire **Dashboard** e verificare i KPI sintetici.
2. Aprire **Forecasting** e selezionare un orizzonte di 6 o 12 mesi.
3. Controllare storico, mediana prevista e confidence band.
4. Aprire **Scenarios** e impostare, per esempio:
   - nuove assunzioni: `150`;
   - aumento salariale: `3%`;
   - smart working: `3 giorni`;
   - riduzione turnover: `10%`.
5. Generare lo scenario e confrontare gli impatti.
6. Aprire **AI Chat**, scegliere il modello Ollama e chiedere:

```text
Quali sono i principali rischi HR nei prossimi 12 mesi?
```

```text
Quale impatto ha lo scenario corrente sul costo del personale?
```

```text
Confronta il trend delle assenze con quello del turnover e proponi tre azioni.
```

7. Verificare che la chat mantenga il contesto nelle domande successive.

---

## 16. Test tecnici

### Test Streamlit

```powershell
python -m streamlit hello
```

### Test Ollama

```powershell
$body = @{
    model = "qwen3:4b"
    prompt = "Rispondi soltanto con: Ollama operativo"
    stream = $false
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:11434/api/generate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Test Timestral

Creare temporaneamente `test_timestral.py`:

```python
import numpy as np
from timestral import TimestralForecaster

model = TimestralForecaster.from_pretrained(
    "mistralai/Timestral-28M"
)

context = np.array(
    [100, 105, 103, 110, 115, 118, 121, 119, 125, 130, 128, 135],
    dtype=np.float32,
).reshape(1, 1, -1)

forecast = model.forecast(context, prediction_length=6)
print("Mediana:", forecast.median)
print("Quantili:", forecast.quantile_levels)
```

Eseguire:

```powershell
python .\test_timestral.py
```

### Test applicativi

Se la cartella `tests` contiene test automatizzati:

```powershell
pip install pytest
pytest -q
```

---

## 17. Memoria della chat

La memoria prevede due livelli:

- **session memory:** conversazione attiva in `st.session_state`;
- **persistent memory:** sessioni e messaggi salvati nel database SQLite.

Percorso predefinito:

```text
storage\hr_future_insights.db
```

Per azzerare completamente la memoria in ambiente demo:

1. Chiudere Streamlit con `Ctrl+C`.
2. Eseguire:

```powershell
Remove-Item .\storage\hr_future_insights.db -ErrorAction SilentlyContinue
```

3. Riavviare la webapp.

> Non cancellare il database se contiene sessioni che si desidera conservare.

---

## 18. Dati sintetici

Il generatore dovrebbe produrre almeno 36-48 mesi di storico per:

- headcount;
- giorni di assenza;
- costo payroll;
- turnover;
- straordinari;
- distribuzione per area organizzativa.

Caratteristiche consigliate:

- seed fisso per demo ripetibili;
- trend di crescita moderato;
- stagionalita annuale sulle assenze;
- correlazione tra headcount e payroll;
- rumore controllato;
- nessun dato personale o riconducibile a dipendenti reali.

Per rigenerare dataset differenti modificare:

```dotenv
SYNTHETIC_DATA_SEED=42
```

---

## 19. Prestazioni e ottimizzazione sul Surface

- Iniziare con `Timestral-5M` o `Timestral-28M`.
- Usare un modello Ollama da 3B/4B su PC con 16 GB RAM.
- Evitare di caricare contemporaneamente piu modelli LLM.
- Chiudere Docker Desktop, Teams e browser con molte schede durante la demo.
- Ridurre `CHAT_MEMORY_MAX_MESSAGES` se la generazione diventa lenta.
- Usare `st.cache_resource` per non ricaricare Timestral a ogni interazione.
- Usare `st.cache_data` per dataset sintetici e trasformazioni ripetitive.

Controllare i modelli attivi:

```powershell
ollama ps
```

Liberare memoria rimuovendo un modello dalla sessione:

```powershell
ollama stop qwen3:4b
```

Rimuovere dal disco un modello non piu necessario:

```powershell
ollama rm qwen3:4b
```

---

## 20. Cambio cartella dei modelli Ollama

I modelli possono occupare diversi GB. Per salvarli, per esempio, in `D:\OllamaModels`:

```powershell
[Environment]::SetEnvironmentVariable(
    "OLLAMA_MODELS",
    "D:\OllamaModels",
    "User"
)
```

Terminare Ollama dall'area di notifica e riavviarlo dal menu Start. Aprire poi un nuovo PowerShell.

---

## 21. Risoluzione problemi

### `python` non riconosciuto

- Chiudere e riaprire PowerShell.
- Provare `py -3.12 --version`.
- Verificare che Python sia nel PATH.

### Attivazione `.venv` bloccata

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### `ollama` non riconosciuto

- Riavviare il terminale dopo l'installazione.
- Verificare Ollama nell'area di notifica.
- Riavviare Windows se il PATH non si aggiorna.

### Connessione rifiutata su `localhost:11434`

```powershell
ollama serve
```

In un'altra finestra:

```powershell
Invoke-RestMethod -Uri "http://localhost:11434/api/tags"
```

### Nessun modello disponibile nella webapp

```powershell
ollama pull qwen3:4b
ollama list
```

Poi aggiornare la pagina Streamlit.

### Timestral non si importa

```powershell
pip uninstall timestral -y
pip install git+https://github.com/mistralai/timestral.git
python -c "from timestral import TimestralForecaster; print('OK')"
```

### Errore PyTorch su Surface ARM64

- Verificare che Python e i pacchetti abbiano la stessa architettura ARM64.
- Consultare il selettore PyTorch ufficiale.
- Se non e disponibile una build compatibile, usare temporaneamente il fallback statistico della webapp oppure un ambiente WSL2 compatibile.

### Streamlit non apre il browser

```powershell
python -m streamlit run app.py --server.headless true
```

Aprire manualmente:

```text
http://localhost:8501
```

### Porta 8501 occupata

```powershell
Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue
python -m streamlit run app.py --server.port 8502
```

### La risposta Ollama e troppo lenta

- Selezionare un modello piu piccolo.
- Ridurre la lunghezza della memoria chat.
- Ridurre il contesto inviato al modello.
- Verificare con `ollama ps` se il modello usa CPU o GPU.

---

## 22. Arresto dell'applicazione

Nel terminale Streamlit premere:

```text
Ctrl+C
```

Disattivare l'ambiente virtuale:

```powershell
deactivate
```

Ollama puo restare in background oppure essere terminato dall'icona nell'area di notifica.

---

## 23. Aggiornamento del progetto

Con repository Git configurato:

```powershell
git status
git pull
```

Aggiornare le dipendenze:

```powershell
.\.venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
```

Se `requirements.txt` cambia in modo sostanziale, ricreare l'ambiente:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install git+https://github.com/mistralai/timestral.git
```

---

## 24. Avvio con script PowerShell facoltativo

Creare `start_app.ps1` nella root:

```powershell
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    throw "Ambiente virtuale non trovato. Eseguire prima: python -m venv .venv"
}

. ".\.venv\Scripts\Activate.ps1"

try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 | Out-Null
    Write-Host "Ollama operativo" -ForegroundColor Green
}
catch {
    Write-Warning "Ollama non risponde su http://localhost:11434"
}

python -m streamlit run app.py
```

Esecuzione:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start_app.ps1
```

---

## 25. Packaging Docker facoltativo

Il container Streamlit puo essere costruito con:

```powershell
docker build -t hr-future-insights:local .
```

Esecuzione:

```powershell
docker run --rm -p 8501:8501 `
    -e OLLAMA_BASE_URL=http://host.docker.internal:11434 `
    hr-future-insights:local
```

> Su Windows il container deve usare `host.docker.internal` per raggiungere Ollama eseguito sull'host. Timestral e PyTorch possono aumentare sensibilmente dimensione e tempo di build dell'immagine.

---

## 26. Privacy, sicurezza e uso enterprise

Per il PoC:

- usare solo dati sintetici;
- non caricare dati cliente o informazioni personali;
- mantenere Ollama su `localhost`;
- non esporre Streamlit sulla rete aziendale senza autorizzazione;
- non salvare credenziali SAP nel repository.

Prima di un pilot reale introdurre:

- autenticazione aziendale e RBAC;
- autorizzazioni coerenti con i ruoli HR;
- cifratura dei dati at-rest e in-transit;
- audit log e retention policy;
- pseudonimizzazione/minimizzazione dei dati;
- backtesting e monitoraggio del model drift;
- security assessment e verifica delle licenze dei modelli.

---

## 27. Limiti noti del PoC

- I forecast non sono validati su dati SAP HCM reali.
- Gli insight Ollama dipendono dal modello selezionato e possono contenere errori.
- Timestral fornisce previsioni, non spiegazioni causali.
- Lo Scenario Simulator dimostra l'esperienza utente e non costituisce un motore ufficiale di budgeting.
- Il progetto non sostituisce SAP Analytics Cloud, SAP SuccessFactors People Analytics o sistemi HR autorizzati.

---

## 28. Riferimenti ufficiali

- Timestral GitHub: https://github.com/mistralai/timestral
- Timestral model card: https://huggingface.co/mistralai/Timestral-209M
- Mistral documentation: https://docs.mistral.ai/models/timestral-1-0-209m
- Ollama Windows: https://docs.ollama.com/windows
- Ollama download: https://ollama.com/download/windows
- Ollama API: https://docs.ollama.com/api/introduction
- Streamlit installation: https://docs.streamlit.io/get-started/installation/command-line
- Python Windows: https://www.python.org/downloads/windows/
- PyTorch selector: https://pytorch.org/get-started/locally/

---

## 29. Checklist finale

Prima dell'avvio verificare:

- [ ] Python 3.12 disponibile.
- [ ] Git disponibile.
- [ ] Ambiente `.venv` creato e attivo.
- [ ] `requirements.txt` installato.
- [ ] PyTorch e Timestral importabili.
- [ ] Ollama in esecuzione su `localhost:11434`.
- [ ] Almeno un modello Ollama installato.
- [ ] File `.env` configurato.
- [ ] Cartella `storage` scrivibile.
- [ ] Nessun dato reale o riservato inserito nel PoC.
- [ ] Webapp raggiungibile su `http://localhost:8501`.

---

## 30. Comandi essenziali riassuntivi

```powershell
cd C:\Projects\hr-future-insights
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install "torch>=2.4"
pip install git+https://github.com/mistralai/timestral.git
ollama pull qwen3:4b
python -m streamlit run app.py
```

Applicazione:

```text
http://localhost:8501
```

---

## License e responsabilita

Il codice applicativo deve utilizzare la licenza definita dal repository del progetto. Il codice Timestral e i relativi pesi hanno licenze distinte: verificare sempre i file `LICENSE` ufficiali prima di un utilizzo commerciale o enterprise. I modelli Ollama mantengono le rispettive licenze, che devono essere verificate singolarmente.

---

**HR Future Insights**  
_Dai dati di oggi alle persone di domani._
