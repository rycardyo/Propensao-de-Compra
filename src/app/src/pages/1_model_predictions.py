import streamlit as st
import pandas as pd 
import sys 
from pathlib import Path
import os 

root_path = Path(__file__).resolve().parents[2]
sys.path.append(os.path.join(root_path, 'model/src'))

from model_prediction  import RankerModel
from data_preparation  import DataPreparation

st.set_page_config(
    layout='wide'
)

st.title('Ranked List')
st.markdown(''' Lista de clientes rankeados por propensão de compra (%)''')

def add_status_column(dataset):
    if 'Status' not in dataset.columns:
        dataset['Status'] = 'Pendente'
    
    return dataset 

def get_inferenced_dataset():
    dataset = pd.read_csv(st.query_params['datasetFPath'])
    return dataset 


def get_inference_dataset():
    dataset = pd.read_csv(st.query_params['datasetFPath'])
    dataset_columns = [x for x in dataset.columns if x not in ['Unnamed: 0', 'unnamed: 0','id','response']]
    dataset = dataset[dataset_columns]

    data_preparator = DataPreparation(dataset, verbose = True)
    dataset_to_model = data_preparator.pipeline()

    model = RankerModel()
    propensity_to_buy = model.predict(dataset_to_model)

    dataset['Propensity_to_buy'] = propensity_to_buy * 100
    dataset['Propensity_to_buy'] = dataset['Propensity_to_buy'].apply(lambda x: round(x,2))
    dataset = dataset.sort_values(by = 'Propensity_to_buy', ascending = False)

    return dataset 


def get_dataset(action):
    if action == 'inference':
        return get_inference_dataset()
    
    if action == 'last_action':
        return get_inferenced_dataset()
    

    if action == 'insuranceHealthCross':
        return get_inferenced_dataset()
    

    raise ValueError('Nao foi possivel retornar o dataset, os parametros permitidos são [last_action, inference]')


dataset = get_dataset(st.query_params['action'])
dataset = add_status_column(dataset)

columns_disabled = [x for x in dataset.columns if x != "Status"]

dataset_result   = st.data_editor(
    dataset, 
    column_config = {
                        "Status" : st.column_config.SelectboxColumn(
                            "Resultado da proposta",
                            help = "Insira aqui o resultado do contato feito com o cliente",
                            options=[
                                "🫀 Aceita",
                                "Aceita com desconto",
                                "Pendente",
                                "Rejeitada"
                            ],
                            required=True,
                        )
            },
    disabled = columns_disabled,
    hide_index=True
    )

salvar_resultado = st.button(label = "Save Results")
saveFPath = os.path.join(root_path, 'data/actions/lastAction/results.csv') if st.query_params['action'] != 'insuranceHealthCross' else os.path.join(root_path, 'data/actions/insuranceHealthCross/results.csv') 

if salvar_resultado:
    dataset_result.to_csv(saveFPath)
    st.success('Resultado salvo com sucesso', icon="✅")
