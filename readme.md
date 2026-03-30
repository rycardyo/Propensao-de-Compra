# Avaliação da propensão de crosseling dos clientes de uma seguradora de saúde. 

## 1.0 Desafio: 
A empresa Você Mais Seguro fornece planos de saúde e seguros de vida. 
A empresa está interessada em lançar um novo seguro de veiculos e acredita no potencial que possuí dos clientes em sua base. 
Em uma primeira etapa, foi realizada uma grande pesquisa com uma parcela de seus clientes para entender quais destes clientes estariam interessados em adquirir o novo seguro de veiculos.

No entando, restam mais de 80 mil clientes ainda não abordados, além dos novos clientes que vem entrando na base. O CFO já informou ao diretor comercial que havia orçamento para contatar apenas 20 000 dos mais de 80 000 clientes ainda não abordados. 

Para lidar com o  desafio de bater a meta de vendas do comercial para o novo produto e ainda assim manter a conformidade orçamentária, o diretor comercial solicitou ao time de dados um produto capaz de identificar os clientes que realmente desejam adquirir o seguro veicular, para garantir que sua ação com 20 000 clientes seja o mais assertiva possível. 

Para resolver este problema nasceu este projeto, uma solução capaz de avaliar o indice de propensão de compra de cada cliente da base, que se mostrou **300% mais assertivo** que uma abordagem aleatória e **30% mais acurado** que a melhor premissa de negócio, com potencial de alavancar o faturamento anual estimado da ação em **R$ 8 Milhões** caso fosse usada a **abordagem aleatória** e em  **R$ 3 Milhões no caso de uso da melhor premissa de negócio**

O modelo final, foi disponibilizado em uma aplicação web, a qual é acessível via url: 
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

        - **Recomendação:** Avaliar se as ações de construção de relacionamento realizadas pelo CS estão sendo efetivas, uma vez que a confiança do cliente na marca aparenta não crescer com seu tempo na base. 


### 2.2 - Modelagem em top ranking e metricas de avaliação. 

O problema em pauta, exige uma solução de rankeamento. A idéia central por trás de algoritmos de rankeamento esta em se atribuir um score (a cada a mostra do dataset) capaz de representar quantitativamente, o quanto que um cliente possui de probabilidade de adquirir um seguro veicular. A este score, demos o nome de "propensão de compra" 

Com cada um dos clientes possuindo uma feature de propensão de compra, a tarefa de rankeamento torna-se simplesmente ordenar a lista do maior para o menor. Ou seja, o desafio do projeto é encontrar uma maneira de gerar de nabeura assertuva, esta probabilidade para cada cliente.

**2.2.1 - Modelando probabilidades** 

Para  o desafio de modelar as probabilidades de propensão de compra, podemos utilizar algoritmos classicos de classificação, uma vez que os mesmos em sua essencia, apenas modelam uma probabilidade de cada amostra pertencer a cada uma das classes. Neste caso, nossas "classes" são se o cliente vai ou não adquirir um seguro veicular, e o algoritmo estima a probabilidade dos eventos "compra o seguro" e "não compra o seguro" acontecer.

Durante o projeto foram realizados testes com os seguintes algoritmos:
    * Random Forest
    * Regressão Logistica 
    * KNN Classifier
    * Redes Neurais Artificiais
    * xGboost 

Sendo, o modelo que apresentou melhor desempenho (e o modelo escolhido) o xGboost. 

**2.2.2 - Avaliando modelos de rankeamento** 

Diferente do processo de se avaliar um algoritmo de classificação sob a ótica/objetivo de apenas classificar uma amostra, onde métricas como accuracy, precision, recall, auc, f1 - score, geralmente são suficientes para se avaliar o desempenho final do modelo, para problemas de rankeamento o jogo muda. 

No cenário de rankeamento estamos interessados não na classificação em si, mas no score de probabilidade que o modelo atribui a cada amostra, por isso métricas como:
    * Top k Precision - Onde avalia-se a precisão do modelo para um top k itens rankeados, onde k, é o tamanho da amostra a ser avaliada.
    * Top k Recall    - Onde avalia-se a precisão do modelo para um top k itens rankeados, onde k, é o tamanho da amostra a ser avaliada.

Para nosso problema, onde o objetivo é maximizar a conversão dos 20 mil clientes contatados, desejamos otimizar nossa top 20k precision, o que irá garantir que ao escolher 20 mil clientes para entrar em contato, seja possível garantir que teremos o maior número de conversões. 

Para os 20k Clientes, o xgBoost apresentou o resultado:

| model | precision_top_20k | customers | Revenue |
| :---  | :---: | :---: | :--- |
| XGBoost | 0.33585 | 6717 | R$ 12.125.078.36 |
| Afraid_Business_Perspective | 0.25945 | 5189 | R$ 9.366.835.14 |
| RFM_Business_Perspective | 0.21835 | 4367 | R$ 7.883.015.81 |
| Demographic_Business_Perspective | 0.16470 | 3294 | R$ 5.946.108.10 |
| Random Guess | 0.12270 | 2454 | R$ 4.429.796.38 |


### 2.4 - Data APP com da solução
    - Docker Container
    - Streamlit
    - Avaliable at:

-----
### 3. Resultados 
    #### Premissas de negócio envolvidas na comparação 
    #### Tabela coparativa. 
    #### ...