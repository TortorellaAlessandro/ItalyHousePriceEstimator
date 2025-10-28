import joblib
import pandas as pd
import streamlit as st
import math

REGRESSOR = joblib.load("HousePredictionregressor.pkl")

def generate_tipo_immobile(tipo: str):
    match tipo:
        case "Villa":
            tipo_immobile = (1, 0)
        case "Appartamento":
            tipo_immobile = (0, 1)
        case _:
            tipo_immobile = (0, 0)
    return tipo_immobile

def generate_input(superficie, stanze, bagni, regione, citta, portiere, villa, appartamento):
    
    p = 1 if portiere == "Sì" else 0
    bps = float(int(bagni)/int(stanze)) if int(stanze) != 0 else 0
    srfroom = float(int(superficie)/int(stanze)) if int(stanze) != 0 else 0

    df = pd.DataFrame([{
        "superficie" : int(superficie),
        "stanze" : int(stanze),
        "bagni" : int(bagni),
        "regione" : regione.lower(),
        "citta" : citta,
        "portiere" : p,
        "villa" : villa,
        "appartamento" : appartamento,
        "bagni per stanza" : bps,
        "superficie/stanze" : srfroom
    }])
    

    return df


st.set_page_config(
    page_title="Stima Prezzo Case",
    layout="wide"
)

st.title("Stimatore prezzo immobile")

variables, target = st.columns(2)

with variables:
    # TODO: Aggiungi valori di default ai vari componenti per evitare errori oppure metti valori di default nella funzione

    generate_target = False

    superficie = st.text_input("Superficie immobile:", placeholder= "0")
    stanze = st.text_input("Numero stanze:", placeholder= "0")
    bagni = st.text_input("Numero bagni:", placeholder= "0")

    regione = st.text_input("Regione immobile:")
    citta = st.text_input("Citta immobile:")

    opzioni = ["Sì", "No"]
    portiere = st.segmented_control("Presenza portiere:", options= opzioni, selection_mode= "single")

    tipo_immobile = st.selectbox(
        "Indica il tipo di immobile:",
        ("Villa", "Appartamento", "Altro")
    )

    btn = st.button("Calcola prezzo immobile")
    if btn:
        immobile = generate_tipo_immobile(tipo_immobile)
        regressor_input = generate_input(superficie, stanze, bagni, regione, citta, portiere, immobile[0], immobile[1])
        generate_target = True

with target:
    if generate_target:
        estimate = REGRESSOR.predict(regressor_input)
        price = math.trunc(float(estimate))
        error = price * 0.35
        st.header(f"Prezzo stimato tra i: {price+error: ,.0f}€ e {price-error: ,.0f}€".replace(",", "."))