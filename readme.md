# Avaliação da propensão de crosseling dos clientes de uma seguradora de saúde. 

## 1.0 Desafio: 
A empresa Você Mais Seguro fornece planos de saúde e seguros de vida. 
A empresa está interessada em lançar um novo seguro de veiculos e acredita no potencial que possuí dos clientes em sua base. 
Em uma primeira etapa, foi realizada uma grande pesquisa com uma parcela de seus clientes para entender quais destes clientes estariam interessados em adquirir o novo seguro de veiculos.

No entando, restam mais de 80 mil clientes ainda não abordados, além dos novos clientes que vem entrnado na base. O CFO já informou ao diretor comercial que havia orçamento para contatar apenas 20 000 dos mais de 80 000 clientes ainda não abordados. 

Para lidar com o  desafio de bater a meta de vendas do comercial para o novo produto e ainda assim manter a conformidade orçamentária, o diretor comercial solicitou ao time de dados um produto capaz de identificar os clientes que realmente desejam adquirir o seguro veicular, para garantir que sua ação com 20 000 clientes seja o mais assertiva possível. 

Para resolver este problema nasceu este projeto, uma solução capaz de avaliar o indice de propensão de compra de cada cliente da base, que se mostrou **300% mais assertivo** que uma abordagem aleatória e **30% mais acurado** que a melhor premissa de negócio, com potencial de alavancar o faturamento anual estimado da ação em **R$ 8 Milhões** caso fosse usada a **abordagem aleatória** e em  **R$ 3 Milhões no caso de uso da melhor premissa de negócio**

Fonte Dataset: 


------ 
## 2.0 Descrição da solução

### 2.1 - EDA (Exploratory Data Analisys) - Top Insigths 

* 1. Clientes com veiculos mais antigos no geral, possuem uma maior tendencia a adquirir o seguro.

* 2. Clientes que já possuem seguro veicular, possuem uma propensão de compra muuito menor, quando comparados a clientes que ja possuem seguro. 

* 3. Clientes que ja tiveram algum sinistro registrado, possuem uma propensão maior a adquirir um seguro veicular. 

* 4. A regiao 28 concentra quase metade (42%) dos clientes com intenção de adquirir um 
seguro veicular. 

* 5. Clientes na faixa de 30-40 anos são mais propensos a adquirir um seguro, quando comparado aos demais grupos de idade.

* 6. Não há relação entre o tempo do cliente na base e sua propensão em adquirir um seguro veicular. 
    - **Recomendação:** Avaliar se as ações de construção de relacionamento realizadas pelo CS estão sendo efetivas, uma vez que a confiança do cliente na marca
    aparenta não crescer com seu tempo na base. 


### 2.2 - Feature Egeneering 

### 2.3 - Modelagem em top ranking e metricas de avaliação. 
    - 
### 2.4 - Data APP com da solução
    - Docker Container
    - Streamlit
    - Avaliable at:

-----
### 3. Resultados 
    #### Premissas de negócio envolvidas na comparação 
    #### Tabela coparativa. 
    #### ...