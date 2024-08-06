import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pywhatkit as kit
import os

# Função para gerar a escala
def generate_schedule(start_date, people):
    dates = pd.date_range(start=start_date, periods=365)
    schedule = [(date, people[i % len(people)]) for i, date in enumerate(dates)]
    return pd.DataFrame(schedule, columns=["Data", "Pessoa Escalada"])

# Função para enviar mensagem no WhatsApp

def enviar_mensagem(numero, mensagem, hora, minuto):

    kit.sendwhatmsg(numero, mensagem, hora, minuto)

# Lista de pessoas
people = ["Neres", "Alex", "Ruth"]

# Data de início da escala
start_date = datetime.now().date()

# Interface do Streamlit
st.title("Escala para lavar a louça")

# Inicializa ou carrega a escala
if os.path.exists("schedule.csv"):
    df = pd.read_csv("schedule.csv")
else:
    df = generate_schedule(start_date, people)
    df.to_csv("schedule.csv", index=False)

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

# Widget para selecionar data
selected_date = st.date_input("Selecione uma data", datetime.now().date())

# Filtrar escala por data selecionada
if not df.empty:
    filtered_schedule = df[df["Data"] == selected_date.strftime("%Y-%m-%d")]
    if not filtered_schedule.empty:
        person = df[df["Data"] == selected_date.strftime("%Y-%m-%d")]["Pessoa Escalada"].values[0]
        st.success(f'## Olá {person}, \n ### você está escalado para lavar a louça nesta data.')

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


if st.button("Enviar Mensagem de WhatsApp"):
    if not df.empty:
        try:
            person = df[df["Data"] == selected_date.strftime("%Y-%m-%d")]["Pessoa Escalada"].values[0]
            st.success(f"Enviando mensagem para {person}")
            if person == "Alex":
                phone_number = '+5577991395904'  # Substitua pelo número de telefone desejado
                enviar_mensagem(phone_number, f'Olá {person}, você está escalado para lavar a louça hoje.', hora,
                                minuto)
            elif person == "Neres":
                phone_number = '+5577991084570'  # Substitua pelo número de telefone desejado
                enviar_mensagem(phone_number, f'Olá {person}, você está escalado para lavar a louça hoje.', hora,
                                minuto)
            elif person == "Ruth":
                phone_number = '+5577991278896'  # Substitua pelo número de telefone desejado
                enviar_mensagem(phone_number, f'Olá {person}, você está escalado para lavar a louça hoje dia {dia}/{mes}.', hora,
                                minuto)


        except IndexError:
            st.warning("Nenhuma pessoa encontrada para a data selecionada.")
    else:
        st.warning("Escala não encontrada. Por favor, gere a escala primeiro.")



# Mostrar a escala
if st.checkbox("Mostrar Escala Atual"):
    st.write(df)
