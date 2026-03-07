import streamlit as st 
import pandas as pd 
import json
import os 
from datetime import datetime

def check_columns(df):
    with open('../model/resources/dataset/.required_columns.json', 'r') as f:
        required_columns = json.load(f)["required_columns"]

    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f'Missing columns: {", ".join(missing_columns)}')
        return False

    return True


uploaded_file = st.file_uploader('Upload a customers list', type = ['csv', 'xlsx'])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if check_columns(df):
        st.dataframe(df.sample(frac=.7))

make_predictions = st.button('Make Predictions')

if make_predictions:
    try:
        df.fillna(value = '', inplace=True)
        attatchedFName = datetime.now().strftime('%d_%m_%Y %H-%M:-%s')
        attatchedFPath = f'./payload_items/{attatchedFName}.csv'
        json_df = df.to_csv(attatchedFPath) 
        
        st.switch_page('pages/1_model_predictions.py', 
                    query_params={'datasetFName' : attatchedFPath})
        
    except NameError:
        st.warning('Para realizar predições, é necessário que um arquivo seja enviado.Por favor, anexe um arquivo e tente novamente')

    
