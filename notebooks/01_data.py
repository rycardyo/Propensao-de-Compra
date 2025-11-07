# %% [markdown]
# # Desafio

# %% [markdown]
# A empresa Você Mais Seguro fornece planos de saúde e seguros de vida. 
# A empresa está interessada em lança um novo seguro de veiculos, e desja entender a propensão de compra de seus clientes para este novo cenário. 
# Em uma primeira etapa, foi realizada uma grande pesquisa com seus cleintes, para entender quais destes clientes estariam interessados em adquirir o novo seguro de veiculos.
# 
# Agora, com novos clientes do plano de saude entrando para sua base, a empresa deseja entender quais destes novos clientes teriam maior propensão de compra do novo seguro de veiculos.
# No entanto, a empresa não esta interessada em gastar com pesquisas para todos os novos clientes, e sim apenas para aqueles que tem maior propensão de compra, 
# haja visto,que seu efetivo comercial, não é capaz de entrar em contato, para fornecer um processo de pré vendas personalizado para toda a base de seus novos clientes, somente
# para 2000 deles de cada vez. 
# 
# Para isso, este projeto tem como objetivo apresentar uma lista, com os 2000 clientes com maior probabilidade de venda do seguro de veículos.

# %% [markdown]
# # 0.0 Imports

# %%
import pandas as pd 
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import os 

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# %% [markdown]
# ### 0.1 Helper Functions

# %%
def jupyter_settings():
    %matplotlib inline
    %pylab inline

    plt.style.use( 'bmh' )
    plt.rcParams['figure.figsize'] = [25, 8]
    plt.rcParams['font.size'] = 24
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    pd.set_option( 'display.expand_frame_repr', False )
    sns.set()

jupyter_settings()

def print_descriptive_stats(df,
                            column):
    print(f'**Clientes que adquiririam o Seguro - {column} statistics**')
    print(df[df.Response == 1][column].describe())
    print('-'*45)
    print(f'**Clientes NAO que adquiririam o Seguro - {column} statistics**')
    print(df[df.Response == 0][column].describe())
    print('\n')

def get_frequency_table(df, column): 

    df_frequency_1 = df[df.Response == 1].groupby(column).Response.count().reset_index()
    df_frequency_1.rename(columns={'Response':'Count_Response_1'}, inplace=True)


    df_frequency_0 = df[df.Response == 0].groupby(column).Response.count().reset_index()
    df_frequency_0.rename(columns={'Response':'Count_Response_0'}, inplace=True)

    df_frequency = pd.merge(df_frequency_1, df_frequency_0, on=column, how='inner') 
    df_frequency['Total'] = df_frequency['Count_Response_1'] + df_frequency['Count_Response_0']
    df_frequency['Propensity_to_buy'] = df_frequency['Count_Response_1']/df_frequency['Total']
    df_frequency['%_sample_to_buy'] = df_frequency['Count_Response_1']/df_frequency['Count_Response_1'].sum() 
    df_frequency['%_sample_to_not_buy'] = df_frequency['Count_Response_0']/df_frequency['Count_Response_0'].sum() 
    df_frequency['%_sample_size']   = df_frequency['Total']/len(df)
    df_frequency['%_general_propensity_to_buy'] = len(df[df.Response==1])/len(df)
    
    return df_frequency

# %% [markdown]
# # 1.0 Limpeza dos Dados

# %% [markdown]
# **Tipos de limpezas**
# 
# * Nulos
# * Tipagem inconsistente 
# * Claros outliers (indicio de erro de digitação)
# 

# %% [markdown]
# ### 1.1 - Conhecendo o Dataset

# %%
df_raw = pd.read_csv(os.path.join(f'{BASE_PATH}/data/raw/data.csv'))
df_raw.head()

# %% [markdown]
# **Features e NaN** 

# %%
df_raw.info()


# %% [markdown]
# Não há NaN no dataset

# %% [markdown]
# ----
# 
# **Descrevendo algumas features**
# 
# ---- 
# 
# **Vintage:** - Tempo em dias, que o cliente esta na base da empresa.
# 
# **Policy Sales Channel** - Canal de contato com o cliente
# 
# **Vehicle_Damage:** - O Cliente ja teve algum dano em seu veiculo? 
# 
# **Previously Insured:** - O cliente já possuí algum seguro veicular?
# 
# 

# %% [markdown]
# ### 1.2 - Validando os valores de cada coluna
# 
# Aqui o objetivo é compreender o valor presente em cada coluna, e se halguma coluna, não possuí algum valor de tipo inconsistente: 
# 
# **Exemplo:** idade possui valores do tipo string

# %%
cols_to_evaluate = df_raw.columns
cols_to_evaluate = cols_to_evaluate.drop(['id'])
cols_to_evaluate

for col in cols_to_evaluate:
    print('---'*20)
    print(col)
    print(df_raw[col].value_counts())

# %% [markdown]
# #### Conclusões

# %% [markdown]
# **Não foi identificada inconsistencia de tipagem**
# 
# Aqui não considerei a idade do veiculo (> 1 year...) como inconsistencia, uma vez que a ideia do campo, é realmente ser um campo do tipo texto.

# %% [markdown]
# ### 1.3 - Identificando outliers claros que indicam falha no preenchimento dos dados

# %%


# Your DataFrame and column list would be defined here
# Example: df_raw = pd.DataFrame(...)
# Example: cols_to_evaluate = ['col_name_1', 'col_name_2']

for col in cols_to_evaluate:
    if df_raw[col].dtype in ('int64', 'float64'):
        # 1. Define the figure size
        plt.figure(figsize=(18, 4))
        
        # 2. BOXPLOT: Position 1 of 2
        plt.subplot(1, 2, 1) # <--- Corrected this to be 1, 2, 1
        sns.boxplot(x=df_raw[col])
        plt.title('Box Plot') # Optional: Add a title to the subplot
        
        # 3. HISTOGRAM: Position 2 of 2
        plt.subplot(1, 2, 2) # <--- Corrected this to be 1, 2, 2
        sns.histplot(x=df_raw[col], kde=True)
        plt.title('Histogram') # Optional: Add a title to the subplot
        
        # 4. Main title and display
        plt.suptitle(f'Distribution of {col}', fontsize=16) # Using f-string for clarity
        plt.tight_layout(rect=[0, 0, 1, 0.95]) # Adjust layout to prevent suptitle overlap
        plt.show()

# %% [markdown]
# ##### Conclusões

# %% [markdown]
# Apesar do campo Annual Premium, possuir claros outliers, isso não indica uma falha real no preenchimento dos dados, apenas expõe que existem clientes com valores de premio absurdamente maiores que outros (algo totalmente coerente/possível de ocorrer em uma seguradora de saúde)

# %%


# %% [markdown]
# # 2.0 Exploração dos dados

# %% [markdown]
# ## 2.0.1 - Separação do dataset
# 
# Como possuímos uma boa quantidade de amostras, para evitar que a consutrução/modelagem do problema sofra algum vies inserido por algum conhecimento adquirido na análise exploratória, vamos separar o dataset em treino, teste e validação neste momento. Desta forma garantimos que não havera nenhum tipo de vazamento de dados 
# 

# %%
df_train, df_test = train_test_split(df_raw, test_size=0.2, random_state=42)
df_train, df_val = train_test_split(df_train, test_size=0.2, random_state=42)

print(f'Train shape: {df_train.shape}'
      f'\nValidation shape: {df_val.shape}' 
      f'\nTest shape: {df_test.shape}')

df_1 = df_train.copy()
df_1.head()

# %% [markdown]
# ## 2.1 - Mapa de hipoteses

# %%
from matplotlib import pyplot as plt
import numpy as np 
from PIL import Image


img = Image.open('./media/propensao_de_compra_mind_map.png')
numpy = np.array(img)

plt.figure(figsize=(20, 10))
plt.imshow(numpy)

# %% [markdown]
# ## 2.2 - Hipoteses:
# 
# 
# **Cliente:**
# 
# 1. ~~Clientes com maior grau de escolaridade possuem maior propensão de compra~~
# 2. ~~Clientes com Veiculos com preço mais elevado possuem maior propensão de compra~~
# 3. Clientes com mais tempo na base, possuem maior propensão de compra
# 4. Clientes com Ticket mais elevado possuem maior propensão de compra 
# 5. Clientes com Veiculos mais novos possuem maior propensão de compra 
# 6. Clientes com seguro veicular possuem menor propensão de compra 
# 7. Existem regiões, onde os clientes possuem maior propensão de compra
# 8. Clientes com veiculos que ja sofreram danos, possuem maior propensão a aquisição do seguro 
# 9. Clientes com mais de 30 anos, são mais propensos a adquirir o seguro.
# 10. ~~Clientes com Salario mais elevado, possuem maior propensão~~
# 11. Clientes do sexo feminino, possuem maior propensão a aquisição de seguros veiculares
# 12. Clientes alcancados pelo canal 2, tem maior propensao de compra
# 
# **Estrategia de comunicação**
# 
# 1. ~~Abordagems em canais de telefonia, elevam a propensão de compra do cliente.~~ 
# 2. ~~Ofertas realizadas a clientes no inicio do dia, elevam a propensão de compra~~
# 3. ~~O agente quiabo, eleva a propensão de compra~~
# 
# **Produto:**
# 
# 1. ~~Seguros com maior relação (valor_cobertura/preço) possuem maior propensão de compra.~~ 

# %% [markdown]
# ## 2.3 - Validando Hipoteses

# %% [markdown]
# ### 2.3.1 - Clientes

# %% [markdown]
# #### H3 - Clientes com mais tempo na base possuem maior propensão de compra
# 
# **Falsa**

# %%
sns.scatterplot(data = df_1,x='Vintage', y='Response')

# %%
df_1[df_1.Response == 1]['Vintage'].describe()

# %%
df_1[df_1.Response == 0]['Vintage'].describe()

# %%
sns.kdeplot(data = df_1, x='Vintage', hue='Response', fill=True, label = 'Response')

# %% [markdown]
# **Conclusão:** Falso, o vintage possuí impacto algum sobre a decisão de adquirir ou não adquirir um seguro veicular

# %% [markdown]
# ### H4. Clientes com ticket mais elevado, possuem maior propensão de compra
# 
# **Conclusão:** Falso, o interesse do cliente em comprar ou não comprar, não é influenciado pelo annual premium pago pelo cliente

# %%
print('**Clientes que adquiririam o Seguro**')
print(df_1[df_1.Response == 1].Annual_Premium.describe())

print('-'*45)
print('**Clientes NAO que adquiririam o Seguro**')

print(df_1[df_1.Response == 0].Annual_Premium.describe())

# %%
sns.kdeplot(data = df_1, x='Annual_Premium', hue='Response', fill=True, label = 'Response')

# %% [markdown]
# ### H5 - Clientes com veículos mais novos possuem maior propensão de compra
# 
# **Conclusão:** Falsa, na realidade clientes com veiculos mais antigos, no geral, possuem uma maior tendencia a adquirir o seguro, que clientes com veículos mais novos

# %%
df_1.Vehicle_Age.value_counts()
df_1.loc[:,'Vehicle_Age'] = df_1.loc[:,'Vehicle_Age'].replace({'< 1 Year':0, '1-2 Year':1, '> 2 Years':2})



df_vehicle_age = get_frequency_table(df_1, 'Vehicle_Age')
df_vehicle_age


# %%
sns.barplot(data=df_vehicle_age, x='Vehicle_Age', y='Propensity_to_buy')

# %% [markdown]
# 

# %% [markdown]
# ### H6 - Clientes com seguro veicular possuem menor propensão de compra
# 
# **Conclusão:** Verdadeira, clientes que já possuem seguro veicular, possuem uma propensão de compra muuito menor, em relação aos que não possuem. Praticamente todos os clientes que disseram comprar o seguro ofertado pela empresa, não possuem um seguro previo > (99%)

# %%
df_previously_insured = get_frequency_table(df_1, 'Previously_Insured')
df_previously_insured

# %%
sns.barplot(data=df_previously_insured, x='Previously_Insured', y='Propensity_to_buy')
plt.title('Propensão de compra x Previously_Insured')

# %% [markdown]
# ### H7. Existem regiões, onde os clientes possuem maior propensão de compra
# 
# **Conclusão:** Sim, ha regiões com maior propensão de compra, que outras, inclusive, a região mais interessate é a região com codigo 28, cujo 18% dos entrevistados comprariam o produto, além da região concentrar cerca de 28% dos entrevistados 

# %%
df_1.Region_Code.nunique()

# %%
df_region_code = get_frequency_table(df_1, 'Region_Code')
df_region_code.sort_values(by='Propensity_to_buy', ascending=False).head(25)

# %%
fig, ax = plt.subplots(figsize=(20,10))
ax.axhline(y=df_region_code.Propensity_to_buy.mean(), color='r', linestyle='--', label='Average Propensity to Buy')
sns.barplot(data=df_region_code, x='Region_Code', y='Propensity_to_buy')
plt.title('Propensão de compra x Region_Code')

# %% [markdown]
# ### H8. Clientes com veiculos que ja sofreram danos, possuem maior propensão a aquisição do seguro 
# 
# **Conclusão** Verdadeiro, clientes que ja tiveram algum tipo de dano veicular, possuem uma tendencia a aquisição de um seguro muito maior, que clientes que nunca tiveram (23% vs 0.5%)

# %%
df_vehicle_damage = get_frequency_table(df_1, 'Vehicle_Damage')
df_vehicle_damage.sort_values(by='Propensity_to_buy', ascending=False)


# %% [markdown]
# ### H9. Clientes com mais de 30 anos, são mais propensos a adquirir o seguro.
# 
# **Conclusão:** Falso, na realidade de fato clientes na faixa dos 30 anos são mais propensos a adquirir um seguro, porem essa propensão se extende somente até os clientes com faixa etaria dos 40 anos, a partir dos 50, essa propensão passa a diminuir
# 

# %%
print_descriptive_stats(df_1, 'Age')

# %%
df_age = get_frequency_table(df_1, 'Age')
df_age.sort_values(by='Propensity_to_buy', ascending=False).head(20)

# %%


# %%
sns.kdeplot(data = df_1, x='Age', hue='Response', fill=True, label = 'Response')

# %%
df_1['faixa_etaria'] = df_1.Age.apply(lambda x: int(x/10)*10)
df_faixa_etaria = get_frequency_table(df_1, 'faixa_etaria')
df_faixa_etaria.sort_values(by = 'Propensity_to_buy', ascending = False)

# %%
sns.kdeplot(data = df_1, x='faixa_etaria', hue='Response', fill=True, label = 'Response')

# %%
sns.lineplot(data = df_faixa_etaria, x = 'faixa_etaria', y = 'Propensity_to_buy',)

# %% [markdown]
# ### H11. Clientes do sexo feminino, possuem maior propensão a aquisição de seguros veiculares
# 
# 
# **Conclusão: Falso**, clientes do sexo masculino, possuem uma probabilidade de comprarem o seguro 3% maiore que homens. 

# %%
df_gender = get_frequency_table(df_1, 'Gender')
df_gender

# %%
sns.barplot(data = df_gender, x='Gender', y='Propensity_to_buy')

# %% [markdown]
# ### H12 - Clientes alcançados pelo canal 2, possuem maior propensão de compra

# %%
df_sales_channel = get_frequency_table(df_1, 'Policy_Sales_Channel')
df_sales_channel.sort_values(by='Propensity_to_buy', ascending=False).head(10)

# %%

df_sales_channel.sort_values(by='Propensity_to_buy', ascending=False).tail(10)

# %%
df_sales_channel.sort_values(by='Propensity_to_buy', ascending = False, inplace=True)
interest_sales_channel =  pd.concat([df_sales_channel.head(10), df_sales_channel.tail(10)])
interest_sales_channel
sns.barplot(data = interest_sales_channel, 
            x='Policy_Sales_Channel', 
            y='Propensity_to_buy')

# %% [markdown]
# ### H13. Clientes sem driving license possuem menor propensão de compra

# %%
df_driving_license = get_frequency_table(df_1, 'Driving_License')
df_driving_license.sort_values(by='Propensity_to_buy', ascending=False)

# %% [markdown]
# ## 2.4 - Análise Multivariada

# %%
df_1.info()

# %% [markdown]
# 

# %%
df_1[['Vehicle_Age','Vintage','Annual_Premium','Age','Response']].corr()

# %% [markdown]
# ### implementing v crammer table

# %%
pd.crosstab(df_1.Vehicle_Age, df_1.Response)

# %%
df_1.count()

# %%
from scipy import stats 

def crammerV(col1 : str, 
             col2 : str,
             df):
    data = pd.crosstab(df[col1], df[col2])
    stat, p, dof, expected = stats.chi2_contingency(data)
    n = data.sum().sum()

    phi_2 = (stat)/n
    r = len(data)
    k = len(data.columns)

    r_til = r - ((r-1)**2)/(n-1)
    k_til = k - ((k-1)**2)/(n-1)
    phi_2_bias = ((k-1)*(r-1))/(n-1)

    phi_til = max(0, phi_2 - phi_2_bias)
    den = min([k_til -1, r_til-1])

    V = np.sqrt(phi_til/den) 

    return V

def plot_crammer(df):

    crammer = pd.DataFrame(index = df.columns, 
                           columns = df.columns)
    
    for col_interest in df.columns:
        for col in df.columns:
            #print('Calculating Crammer V for:', col_interest, 'and', col)
            v = crammerV(col1 = col_interest, 
                         col2 = col,
                         df = df)
            
            crammer.loc[col_interest, col] = v 
    
    crammer.fillna(value = np.nan, 
                   inplace = True)
    
    plt.figure(figsize=(16,6))
    sns.heatmap(
        crammer.astype(float), 
        annot = True, 
        fmt = '.2f'
    )
    return crammer 


# %%
cat_cols = ['Gender','Driving_License','Region_Code','Previously_Insured',
            'Vehicle_Age','Vehicle_Damage', 'Policy_Sales_Channel','faixa_etaria','Age','Response']
df_cat = df_1[cat_cols].copy()

# %%
def chi_2_test(col1 : str, 
               col2 : str,
               df,
               significance_level = 0.05):
    
    data = pd.crosstab(df[col1], df[col2]) 
    stat, p, dof, expected = stats.chi2_contingency(data, lambda_ = "log-likelihood") 

    if p <= significance_level:
        print(f'H0 rejeitada: As variáveis {col1} e {col2} estão associadas, alcançando um p_value de: {p}, com chi_2 de {stat}')
    
    else: 
        print(f'H1 rejeitada: As variáveis {col1} e {col2} não estão associadas, alcançando um p_value de: {p} com chi_2 de {stat}')



# %%
for col1 in cat_cols:
    for col2 in cat_cols:
        if col1 != col2:
            chi_2_test(col1 = col1,
                       col2 = col2,
                       df = df_cat)
            

# %%
cr = plot_crammer(df_cat) 


# %%


# %% [markdown]
# # 3 - Preparação dos dados

# %%
df_3 = df_1.copy()
df_3.info()

# %% [markdown]
# ### 3.1 - Encodings

# %% [markdown]
# #### 3.1.1 - One Hot Encoding (dummi)
# 
# * Policy Sales Channel 
# * Region Code

# %% [markdown]
# **Region Code**

# %% 
# %%
df_region_code = df_3.Policy_df_region_code.copy()
dummies_df_region_code = pd.get_dummies(df_region_code,prefix = "region_code")
dummies_df_region_code.info()


# %%[markdown]
# **Policy Sales Channel**
# %% [markdown]
# ### 3.1.2 - Binary Encoding
# 
# * Gender
# * Driving License
# * Previously Insured
# * Vehicle Damage
# * Response

# %%
df_3.Gender.value_counts()

# %%
map_sexo_feminino = {
    'Male' : 0,
    'Female' : 1 
}

df_3['sexo_feminino'] = df_3.Gender.map(map_sexo_feminino)


# %% [markdown]
# #### 3.1.2 - Region_Code
# 
# **One Hot encoding**
# 
# A justificativa se da pela ausencia de elação quantitativa nos dados de region code. 
# 
# A regiao "102" ser maior que a regiao "32" não faz sentido
# 

# %%


# %% [markdown]
# #### 3.1.3 - Policy Sales Channel
# 
# **One Hot Encoding**

# %%
sales_channel = df_3.Policy_Sales_Channel.copy()
dummies_sales_channel = pd.get_dummies(sales_channel,prefix = "policy_sales_channel")
dummies_sales_channel.info()

# %%
dummies_sales_channel.head(5)

# %%
cat_cols

# %%
df_3_copy = df_3.copy()
df_3_encoded = pd.concat([df_3_copy, dummies_sales_channel, dummies_region_codes], axis = 1)
df_3_encoded.drop(columns = ['Region_Code','Policy_Sales_Channel'], inplace = True)
df_3_encoded.shape

# %%
df_3_copy.info()

# %% [markdown]
# **Conclusão: **

# %%



