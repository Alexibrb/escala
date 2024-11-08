import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# Função para gerar a escala
def generate_schedule(start_date, people):
    dates = pd.date_range(start=start_date, periods=365)
    schedule = [(date, people[i % len(people)]) for i, date in enumerate(dates)]
    return pd.DataFrame(schedule, columns=["Data", "Pessoa Escalada"])

# Lista de pessoas
people = ["Alex", "Neres", "Ruth"]

# Data de início da escala
start_date = datetime.now().date()

# Interface do Streamlit
st.write("# :green[ESCALA]\n ### :blue[para lavar a louça]")
st.write("---")

# Inicializa ou carrega a escala
if os.path.exists("schedule.csv"):
    df = pd.read_csv("schedule.csv")
else:
    df = generate_schedule(start_date, people)
    df.to_csv("schedule.csv", index=False)

password = st.text_input("Digite a senha para ativar as alterações", type="password")
btn_senha = st.button("Ativar")

if btn_senha:
    senha = password.upper()


    if senha == "ANRD":


        col1, col2 = st.columns(2)
        with col1:
            # Botão para gerar a escala
            if st.button("Gerar Escala"):
                df = generate_schedule(start_date, people)
                df.to_csv("schedule.csv", index=False)
                st.write(df)
                st.success("Escala gerada e salva com sucesso!")
        with col2:
            # Botão para apagar a escala
            if st.button("Apagar Escala"):
                if os.path.exists("schedule.csv"):
                    os.remove("schedule.csv")
                    df = pd.DataFrame(columns=["Data", "Pessoa Escalada"])
                    st.success("Escala apagada com sucesso!")
                else:
                    st.warning("Nenhuma escala para apagar.")

    else:
        st.warning("Senha Inválida")


# Widget para selecionar data
selected_date = st.date_input("Selecione uma data:", datetime.now().date())

# Filtrar escala por data selecionada
if not df.empty:
    filtered_schedule = df[df["Data"] == selected_date.strftime("%Y-%m-%d")]
    if not filtered_schedule.empty:
        person = df[df["Data"] == selected_date.strftime("%Y-%m-%d")]["Pessoa Escalada"].values[0]
        st.success(f'## Olá {person}, \n ### Você está escalado para lavar a louça nesta data.')

    else:
        st.warning("Nenhuma entrada encontrada para a data selecionada.")
else:
    st.warning("Nenhuma escala disponível. Por favor, gere a escala primeiro.")




# Entrada do horário
agora = datetime.now()
hora = agora.hour
minuto = agora.minute + 1  # Define o minuto para 1 minuto à frente


dia = agora.day
mes =agora.month


# Mostrar a escala
if st.checkbox("Mostrar Escala Atual"):
    st.write(df)
