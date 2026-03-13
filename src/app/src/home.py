import streamlit as st 
import pandas as pd 
import json
import os 
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
st.set_page_config(
    layout='wide'
)

def check_columns(df):
    with open('../model/resources/dataset/.required_columns.json', 'r') as f:
        required_columns = json.load(f)["required_columns"]

    df.columns = [x.lower() for x in df.columns]    
    missing_columns = [col.lower() for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f'Missing columns: {", ".join(missing_columns)}')
        return False

    return True

def get_last_action_path(actions_path : str = 'data/actions/lastAction'):
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


st.markdown('# O que você deseja fazer hoje? 🗓️')
st.markdown('----')
st.markdown(' ')


_, f1, _ = st.columns([1,2,1]) 
with f1:
    st.markdown('#### Visualizar resultados da campanha Insurance Health Crosselling 📈')
    st.markdown(' ')
    st.markdown(' ')

    insuranceHealthCross = st.button(label = 'Atuar na campanha principal',width=800)

    st.markdown(' ')
    st.markdown(' ')

st.markdown('----')

title1, title2 =  st.columns([2,2], vertical_alignment='bottom')
btn1, btn2     =  st.columns([2,2], vertical_alignment='bottom')

with title1:
    st.markdown("### Dar andamento na ultima ação ⏳" )
    st.markdown("---")
    
with btn1:    
    st.markdown('Continue trabalhando nos clientes adicionados pela ultima vez')
    
    back_to_the_last = st.button(label = "Retomar ultimo Trabalho" ,
                                 width=800)

with title2:
    st.markdown('### Analisar novos clientes 🔎')
    st.markdown('----')
    

with btn2: 
    uploaded_file = st.file_uploader('Upload a customers list', type = ['csv', 'xlsx'])
    make_predictions = st.button('Make Predictions',
                                 width=800)


# Actions

if insuranceHealthCross:
    insuranceHealthCrossFPath = os.path.join(ROOT_PATH, 'data/actions/insuranceHealthCross/results.csv') 

    st.switch_page(
        'pages/1_model_predictions.py',
        query_params={
            'datasetFPath' : insuranceHealthCrossFPath,
            'action'   : 'insuranceHealthCross'
        }
    )


if back_to_the_last:
        if get_last_action_path():
            st.switch_page('pages/1_model_predictions.py', 
                                query_params={'datasetFPath' : get_last_action_path(),
                                            'action' : 'last_action'})

        else:
            st.error('Não ha trabalhos registrados')

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


