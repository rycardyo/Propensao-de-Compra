import streamlit as st 
import pandas as pd 
import json

def check_columns(df):
    required_columns = ['CustomerID', 'Name', 'Email', 'Phone']
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

make_predictiosn = st.button('Make Predictions')
if make_predictiosn:

    df.fillna(value = '', inplace=True)
    json_df = df.to_dict(orient='records') 
    with open('./payload_items/payload.json', 'w') as f:
        
        json.dump(json_df, f, indent=4)

    st.switch_page('pages/1_model_predictions.py')
