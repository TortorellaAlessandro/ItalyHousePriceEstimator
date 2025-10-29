import joblib
import pandas as pd
import streamlit as st
import math

REGRESSOR = joblib.load("HousePredictionregressor.pkl")

def generate_tipo_immobile(tipo: str):
    match tipo:
        case "Villa":
            tipo_immobile = (1, 0, 0, 0, 0, 0)
        case "Appartamento":
            tipo_immobile = (0, 1, 0, 0, 0, 0)
        case "Intera proprieta":
            tipo_immobile = (0, 0, 1, 0, 0, 0)
        case "Attico":
            tipo_immobile = (0, 0, 0, 1, 0, 0)
        case "Loft":
            tipo_immobile = (0, 0, 0, 0, 1, 0)
        case "Mansarda":
            tipo_immobile = (0, 0, 0, 0, 0, 1)
        case _:
            tipo_immobile = (0, 0, 0, 0, 0, 0)
    return tipo_immobile

def convert_bool(to_convert):
    return 1 if to_convert == "Sì" else 0

def generate_input(superficie, stanze, bagni, 
                   regione, citta, 
                   giardino,
                   portiere, posto_auto, cantina, balcone, ultimo_piano,
                   villa, appartamento, intera_proprieta, attico, loft, mansarda):
    
    giardino_comune = 1 if giardino == "Comune" else 0
    giardino_privato = 1 if giardino == "Privato" else 0

    p = convert_bool(portiere)
    pa = convert_bool(posto_auto)
    c = convert_bool(cantina)
    b = convert_bool(balcone)
    up = convert_bool(ultimo_piano)

    bps = float(int(bagni)/int(stanze)) if int(stanze) != 0 else 0
    srfroom = float(int(superficie)/int(stanze)) if int(stanze) != 0 else 0
    
    df = pd.DataFrame([{
        "superficie" : int(superficie),
        "stanze" : int(stanze),
        "bagni" : int(bagni),
        "regione" : regione.lower(),
        "citta" : citta,
        "giardino comune" : giardino_comune,
        "giardino privato" : giardino_privato,
        "portiere" : p,
        "posti auto" : pa,
        "cantina" : c,
        "balcone" : b,
        "ultimo piano" : up,
        "villa" : villa,
        "intera proprieta" : intera_proprieta,
        "attico": attico,
        "loft" : loft,
        "mansarda" : mansarda,
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

    opz_giardino = ["Comune", "Privato", "No"]
    giardino = st.segmented_control("Tipologia di giardino:", options= opz_giardino, selection_mode= "single")

    opzioni = ["Sì", "No"]
    portiere = st.segmented_control("Presenza portiere:", options= opzioni, selection_mode= "single")
    posto_auto = st.segmented_control("Posto auto:", options= opzioni, selection_mode= "single")
    cantina = st.segmented_control("Cantina:", options= opzioni, selection_mode= "single")
    balcone = st.segmented_control("Balcone:", options= opzioni, selection_mode= "single")
    ultimo_piano = st.segmented_control("Ultimo piano:", options= opzioni, selection_mode= "single")

    tipo_immobile = st.selectbox(
        "Indica il tipo di immobile:",
        ("Villa", "Appartamento", "Intera proprieta", "Attico", "Loft", "Mansarda","Altro")
    )

    btn = st.button("Calcola prezzo immobile")
    if btn:
        immobile = generate_tipo_immobile(tipo_immobile)
        regressor_input = generate_input(
            superficie, stanze, bagni, 
            regione, citta, 
            giardino, 
            portiere, posto_auto, cantina, balcone, ultimo_piano,
            immobile[0], immobile[1], immobile[2], immobile[3], immobile[4], immobile[5])
        generate_target = True

with target:
    if generate_target:
        estimate = REGRESSOR.predict(regressor_input)
        price = math.trunc(float(estimate))
        error = price * 0.30
        st.header(f"Prezzo stimato tra i: {price+error: ,.0f}€ e {price-error: ,.0f}€".replace(",", "."))
        st.header(f"Valore stimato: {price: ,.0f}€".replace(",", "."))