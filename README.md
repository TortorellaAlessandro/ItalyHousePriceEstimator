# 🏠 Italy House Price Estimator

Un'app web interattiva sviluppata con **Streamlit** che utilizza un modello di **Machine Learning (Random Forest Regressor)** per stimare il prezzo di un immobile in Italia, sulla base di caratteristiche inserite dall'utente come superficie, numero di stanze, città, presenza del portiere, ecc.

---

## 🚀 Funzionalità

- Interfaccia semplice e intuitiva sviluppata in **Streamlit**
- Predizione del prezzo basata su un modello **RandomForestRegressor**
- Calcolo automatico di feature derivate come:
  - rapporto _bagni per stanza_
  - rapporto _superficie per stanza_
- Visualizzazione del prezzo stimato con range di incertezza
- Possibilità di eseguire la stima in tempo reale senza competenze tecniche

---

## 🧠 Modello di Machine Learning

Il modello è stato addestrato su un dataset immobiliare italiano e ottimizzato tramite **GridSearchCV** con validazione incrociata.  
L’algoritmo utilizzato è un **Random Forest Regressor**, scelto per la sua robustezza nel gestire feature numeriche e categoriali.

### Parametri principali

- `n_estimators = 550`
- `max_depth = 30`
- `min_samples_split = 2`
- `min_samples_leaf = 1`

Il modello finale è stato salvato tramite `joblib` nel file `HousePredictionRegressor.pkl` (non incluso nella repository per motivi di dimensione).

---

## 🧩 Struttura del progetto

ItalyHousePriceEstimator/
│
├── app.py # Applicazione Streamlit principale
├── regressor.ipynb # Notebook di training e tuning del modello
├── data/ # Dataset utilizzati per l'addestramento
│ └── sale.csv
├── .gitignore # File per escludere file pesanti e temporanei
└── README.md # Questo file

---

## 🖥️ Come eseguire il progetto in locale

### 1️⃣ Clona la repository

```bash
git clone https://github.com/TortorellaAlessandro/ItalyHousePriceEstimator.git
cd ItalyHousePriceEstimator
```
