import streamlit as st 
import pandas as pd 
import json
import os 
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]

def check_columns(df):
    with open('../model/resources/dataset/.required_columns.json', 'r') as f:
        required_columns = json.load(f)["required_columns"]

    df.columns = [x.lower() for x in df.columns]    
    missing_columns = [col.lower() for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f'Missing columns: {", ".join(missing_columns)}')
        return False

    return True

def get_last_action_path(actions_path : str = 'data/actions'):
    ''' 
        Verify if exists some file in 'data/actions
    '''

    files = os.listdir(os.path.join(ROOT_PATH, actions_path))
    csv_files = []
    for f in files:
        if f.endswith('.csv'):
            csv_files.append(os.path.join(ROOT_PATH, actions_path, f))
    
    if csv_files != []:
        return csv_files[-1]
    
    return False

col_left, btn1, btn2, col_right = st.columns([2,1,1,2])

with btn1:
    back_to_the_last = st.button(label = "Retomar ultimo Trabalho")
    if back_to_the_last:
        if get_last_action_path():
            st.switch_page('pages/1_model_predictions.py', 
                                query_params={'datasetFPath' : get_last_action_path(),
                                            'action' : 'last_action'})

        else:
            st.error('Não ha trabalhos registrados')

with btn2: 
    uploaded_file = st.file_uploader('Upload a customers list', type = ['csv', 'xlsx'])
    make_predictions = st.button('Make Predictions')


    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        if check_columns(df):
            st.dataframe(df.sample(frac=.7))


    if make_predictions:
        try:
            df.fillna(value = '', inplace=True)
            attatchedFName = datetime.now().strftime('%d_%m_%Y %H-%M:-%s')
            attatchedFPath = f'./payload_items/{attatchedFName}.csv'
            json_df = df.to_csv(attatchedFPath) 
            
            st.switch_page('pages/1_model_predictions.py', 
                        query_params={'datasetFPath' : attatchedFPath,
                                      'action'  : 'inference'})
            
        except NameError:
            st.warning('Para realizar predições, é necessário que um arquivo seja enviado.Por favor, anexe um arquivo e tente novamente')

    
