import streamlit as st
import requests
import pandas as pd
import json 

def call_inference(df):
    df = df.rename(columns={
        'Latitude': 'lat',
        'Longitude': 'lon',
        'Minutos Restantes': 'minutes_remaining',
        'Periodo': 'period',
        'Playoffs': 'playoffs',
        'Distancia do arremesso': 'shot_distance'
    })

    data= {
         "dataframe_records": df.to_dict(orient="records")
    }
    print(data)
    url = "http://127.0.0.1:5001/invocations"

    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print("Status code:", response.status_code)
    print("Prediction:", response.json())

    inference = response.json()
    print(response)
    return inference['predictions'][0]

# Cabeçalho do aplicativo
st.write("""
# Dashboard de Monitoramento da Operação

""")

# Sidebar do aplicativo
st.sidebar.header('Parâmetros do Modelo')
    
def user_input_features():
    lat = st.sidebar.slider('Latitude', 33.543300,34.088300,34.0343)
    lon = st.sidebar.slider('Longitude', -118.486800,-118.049800,-118.1288)
    minutes_remaining = st.sidebar.slider('Minutos Restantes', 2,11,1)
    period = st.sidebar.slider('Periodo', 1,7,2)
    playoffs = st.sidebar.slider('Playoffs', 0, 1, 0)
    shot_distance = st.sidebar.slider('Distancia do arremesso', 7, 50,14)
    data = {'Latitude': lat,
            'Longitude': lon,
            'Minutos Restantes': minutes_remaining,
            'Periodo': period,
            'Playoffs': playoffs,
            'Distancia do arremesso': shot_distance            
            }
    features = pd.DataFrame(data, index=[0])
    return features

# Obter entrada do usuário
df_user = user_input_features()

# Exibir entrada do usuário
st.subheader('Parâmetros do Usuário')
st.write(df_user)

acertou = call_inference(df_user)

st.write(f"Kobe Acertou a cesta? {'Sim!' if acertou else 'Não :-('}")