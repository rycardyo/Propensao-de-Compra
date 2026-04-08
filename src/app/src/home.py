import streamlit as st 
import pandas as pd 
import json
import os 
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]

st.set_page_config(
    page_title="Propensão de Compra",
    page_icon="🚗",
    layout='wide'
)

# --- FUNÇÕES DE VALIDAÇÃO ---
def check_columns(df):
    with open(os.path.join(ROOT_PATH, 'model/resources/dataset/.required_columns.json'), 'r') as f:
        required_columns = json.load(f)["required_columns"]

    df.columns = [x.lower() for x in df.columns]    
    missing_columns = [col.lower() for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f'Colunas ausentes: {", ".join(missing_columns)}')
        return False
    return True

def get_last_action_path(actions_path : str = 'data/actions/lastAction'):
    ''' Verify if exists some file in data/actions '''
    full_path = os.path.join(ROOT_PATH, actions_path)
    
    # Verifica se o diretório existe antes de listar
    if not os.path.exists(full_path):
        return False
        
    files = os.listdir(full_path)
    csv_files = [os.path.join(full_path, f) for f in files if f.endswith('.csv')]
    
    if csv_files:
        return csv_files[-1] # Retorna o mais recente
    return False

def getSampleData():
    content = pd.read_csv(os.path.join(ROOT_PATH, 'model/resources/test/sampleDataset.csv'))
    return content.sample(1).to_csv(index=False).encode('utf-8')


# --- INTERFACE DO USUÁRIO (UI) ---

st.title('O que você deseja fazer hoje? 🗓️')
st.markdown('---')

# 1. DESTAQUE PRINCIPAL
st.markdown('### 📈 Campanha Principal')
st.markdown('Visualize os resultados e atue na campanha **Insurance Health Crosselling**.')

insuranceHealthCross = st.button(
    label='Atuar na campanha principal', 
    type='primary', # Deixa o botão em destaque
    use_container_width=True # Responsivo
)

st.markdown('---')

# 2. AÇÕES SECUNDÁRIAS (Divididas em Cards)
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### ⏳ Retomar Trabalho" )
    st.markdown('Continue trabalhando nos clientes adicionados pela última vez.')
    
    # Adicionando um espaço para alinhar os botões
    st.markdown("<br><br>", unsafe_allow_html=True) 
    
    back_to_the_last = st.button(
        label="Retomar último trabalho",
        use_container_width=True
    )

with col2:
    st.markdown('### 🔎 Analisar Novos Clientes')
    st.markdown('Faça o upload de uma lista (CSV/XLSX) para gerar o score de propensão.')
    
    uploaded_file = st.file_uploader(
        'Upload da lista de clientes', 
        type=['csv', 'xlsx'], 
        label_visibility="collapsed" # Esconde o label padrão para ficar mais limpo
    )
    
    # O botão só fica ativo se um arquivo for anexado (evita o NameError)
    make_predictions = st.button(
        'Gerar Predições',
        use_container_width=True,
        disabled=(uploaded_file is None) 
    )

st.markdown('---')

# 3. RECURSOS ADICIONAIS
st.markdown('### 📥 Recursos Adicionais')
st.download_button(
    label='Baixar dataset de exemplo (Template)',
    data=getSampleData(),
    file_name='sampleDataset.csv',
    mime='text/csv',
    icon=':material/download:',
    use_container_width=True
)

# --- LÓGICA DE ROTEAMENTO (AÇÕES) ---

if insuranceHealthCross:
    insuranceHealthCrossFPath = os.path.join(ROOT_PATH, 'data/actions/insuranceHealthCross/results.csv') 
    st.switch_page(
        os.path.join(ROOT_PATH,'src/pages/1_model_predictions.py'),
        query_params={
            'datasetFPath' : insuranceHealthCrossFPath,
            'action' : 'insuranceHealthCross'
        }
    )

if back_to_the_last:
    last_path = get_last_action_path()
    if last_path:
        st.switch_page(
            os.path.join(ROOT_PATH, 'src/pages/1_model_predictions.py'), 
            query_params={'datasetFPath': last_path, 'action': 'last_action'}
        )
    else:
        st.error('Não há trabalhos anteriores registrados no sistema.')

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if check_columns(df):
        st.success("✅ Arquivo validado com sucesso!")
        with st.expander("Pré-visualizar dados importados"):
            st.dataframe(df.sample(frac=.7))
        
        if make_predictions:
            df.fillna(value='', inplace=True)
            attatchedFName = datetime.now().strftime('%d_%m_%Y_%H-%M-%S') # Removido o %s que pode causar bug no windows/linux misturado
            
            # Garantir que o diretório payload_items existe
            payload_dir = os.path.join(ROOT_PATH, 'src/payload_items')
            os.makedirs(payload_dir, exist_ok=True)
            
            attatchedFPath = os.path.join(payload_dir, f'{attatchedFName}.csv')
            df.to_csv(attatchedFPath, index=False) # Adicionado index=False para não salvar o indice do pandas
            
            st.switch_page(
                'pages/1_model_predictions.py', 
                query_params={'datasetFPath': attatchedFPath, 'action': 'inference'}
            )