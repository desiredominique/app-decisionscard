import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt



# Página inicial
st.set_page_config(
    page_title='Decisions Card',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('Decisions Card')

####### HTML ###########
#st.image('ad_image.jpg')

t_cliente = pd.read_csv('t_cliente_202402071704.csv')

#if st.checkbox('Clique aqui para mostrar o banco de dados utilizado'):
#    st.subheader('t_cliente')
#    st.write(t_cliente)

## QTD DE CONTAS CADASTRADAS ##
st.subheader('Quantidade de contas cadastradas')

contas_cadastradas = len(t_cliente['id_cliente'])

st.text(f'A quantidade de contas cadastradas é {contas_cadastradas}.')

## QTD DE CONTAS ATIVAS ##
st.subheader('Quantidade de contas ativas')
contas_ativas = (t_cliente['fl_status_conta'] == 'A').sum()
st.text(f'A quantidade de contas ativas é {contas_ativas}.')

## QTD DE CONTAS ATIVADAS ##
t_venda = pd.read_csv('t_venda_202402071704.csv')

st.subheader('Quantidade de contas ativadas')
contas_ativadas = t_venda['id_cliente'].nunique()
st.text(f'A quantidade de contas ativadas é {contas_ativadas}.')

## PERCENTUAL DE CONTAS BLOQUEADAS X CONTAS CADASTRADAS
    
st.subheader('Percentual de contas bloqueadas x contas cadastradas')

col1, col2 = st.columns(2)

t_bloqueadas = pd.read_csv('t_bloqueio_cliente_202402071704.csv')

if st.checkbox('Clique aqui para abrir o banco de dados utilizado'):
    st.subheader('t_bloqueadas')
    st.write(t_bloqueadas)  

contas_bloqueadas = (t_cliente['fl_status_conta'] == 'B').sum()
bloqueadas_cadastradas = contas_bloqueadas/contas_cadastradas * 100
st.bar_chart(data=t_cliente['fl_status_conta'].value_counts())

st.text(f'O percentual de contas bloqueadas em relação às contas cadastradas {bloqueadas_cadastradas:.2f}%.')

## QTD/PERCENTUAL DE CONTAS POR SITUAÇÃO ##
st.subheader('Quantidade/Percentual de Contas por Situação')

contas_situacao = t_cliente.groupby(['fl_status_conta']).size().reset_index().rename(columns={'fl_status_conta': 'Status',0: 'Contas'})

if st.checkbox('Clique aqui para abrir as contas por situação'):
    st.write(contas_situacao) 
    
st.bar_chart(data=contas_situacao, x= 'Status', y='Contas') 

contas_inativas = (t_cliente['fl_status_conta'] == 'I').sum()

inativas_cadastradas = contas_inativas/contas_cadastradas * 100

ativas_cadastradas = contas_ativas/contas_cadastradas * 100

st.text(f'O percentual de contas ativas em relação às contas cadastradas {ativas_cadastradas:.2f}%.')
st.text(f'O percentual de contas bloqueadas em relação às contas cadastradas {bloqueadas_cadastradas:.2f}%.')
st.text(f'O percentual de contas inativas em relação às contas cadastradas {inativas_cadastradas:.2f}%.')

##  DISTRIBUIÇÃO DE CONTAS POR ORIGEM COMERCIAL ##
st.subheader('Distribuição de Contas por Origem Comercial')

#tab_c_origem = pd.crosstab(t_cliente.id_origem_comercial, t_cliente.id_cliente.count(), rownames=['Id Comercial'], colnames=['Contas'])
contas_origem = t_cliente.groupby(['id_origem_comercial'])['id_cliente'].size().reset_index().rename(columns={'id_origem_comercial': 'Origem', 'id_cliente': 'Qtd'})

if st.checkbox('Clique aqui para abrir a Distribuição de Contas por Origem Comercial'):
    st.write(contas_origem) 

st.bar_chart(data=contas_origem, x='Origem', y='Qtd')

## RANKING DOS CLIENTES POR QTD/VLR COMPRAS ##
st.subheader('Ranking dos Clientes por Quantidade/Valor Compras')
    
clientes_compras = t_venda.groupby('id_cliente')['vl_principal'].sum().sort_values(ascending=False)
if st.checkbox('Clique aqui para abrir o Ranking dos Clientes por Qtd/Vlr Compras'):
    st.write(clientes_compras) 

## QTD CARTÕES ##
st.subheader('Quantidade de Cartões')

t_cartao = pd.read_csv('t_cartao_202402071644.csv')

t_cartao.groupby(t_cartao['id_cartao']).size().sort_values(ascending=True) ##para avaliar se não tem nenhum repetido

cartoes = t_cartao['id_cartao'].nunique()

st.write(f'A quantidade de cartões cadastrados é de {cartoes}.')

## QTD CARTÕES POR SITUAÇÃO ##
st.subheader('Quantidade de Cartões por Situação')
cartoes_situacao = t_cartao.groupby(['fl_status_cartao'])['id_cartao'].size().reset_index().rename(columns={'fl_status_cartao': 'Status', 'id_cartao': 'Qtd'})

if st.checkbox('Clique aqui para abrir a tabela de cartões-situação'):
    st.write(cartoes_situacao)

st.bar_chart(data=cartoes_situacao, x= 'Status', y='Qtd')    

## QTD CARTÕES POR TIPO DE BLOQUEIO ##
st.subheader('Quantidade de Cartões por Tipo de Bloqueio')
t_bloqueio_cartao = pd.read_csv('t_bloqueio_cartao_202402071704.csv')
cartoes_bloqueio = t_bloqueio_cartao.groupby('id_tipo_bloqueio_cartao')['id_cartao'].nunique().reset_index().rename(columns={'id_tipo_bloqueio_cartao': 'Tipo de Bloqueio', 'id_cartao': 'Qtd'})

if st.checkbox('Clique aqui para abrir a tabela de cartões-bloqueio'):
    st.write(cartoes_bloqueio)
    
st.bar_chart(data=cartoes_bloqueio, x= 'Tipo de Bloqueio', y='Qtd') 

## ANALÍTICO DAS CONTAS EM ATRASO ##
st.subheader('Analítico das contas em atraso')

# tabelas para adicionar
t_cobranca = pd.read_csv('t_cobranca_202402071704.csv')

t_fatura = pd.read_csv('t_fatura_202402071704.csv')

#t_bloqueadas = pd.read_csv('t_bloqueio_cliente_202402071704.csv')

t_pagamento_fatura = pd.read_csv('t_pagamento_fatura_202402071704.csv')

# criação de novas tabelas
new_table1 = {'id_cliente': t_cliente['id_cliente'], 'nm_cliente': t_cliente['nm_cliente'], 'id_origem_comercial': t_cliente['id_origem_comercial']}

id_nome_oc = pd.DataFrame(data=new_table1)

new_table2 = {'id_cliente': t_bloqueadas['id_cliente'], 'dt_vencimento': t_bloqueadas['dt_vencimento_fatura']}

dt_venc = pd.DataFrame(data=new_table2)

new_table3 = {'id_cliente': t_fatura['id_cliente'], 'vl_fatura': t_fatura['vl_fatura']}

vl_fatura = pd.DataFrame(data=new_table3)

new_table4 = {'id_cliente': t_pagamento_fatura['id_cliente'], 'dt_pagamento': t_pagamento_fatura['dt_pagamento'], 'vl_pagamento': t_pagamento_fatura['vl_pagamento']}

dt_vl = pd.DataFrame(data=new_table4)

# união das tabelas
new12 = pd.merge(id_nome_oc, dt_venc, on='id_cliente')

new34 = pd.merge(vl_fatura, dt_vl, on='id_cliente')

new1234 = pd.merge(new12, new34, on='id_cliente')
new1234.columns = ['Id Cliente', 'Nome Cliente', 'Id Origem Comercial', 'Data Vencimento', 'Valor Fatura', 'Data Pagamento', 'Valor Pagamento']

if st.checkbox('Clique aqui para abrir a tabela do analítico'):
    st.write(new1234)
    
    
    

######################################### DATAS #########################################
st.subheader('Quantidade de contas sem Compras há + de 90 dias')
    
# Separar data e hora
t_venda[['data_venda', 'hora_venda']] = t_venda['dt_venda'].str.split(' ', expand=True)

## Criação do dataframe com data e id cliente
sem_compras_90d = {'data': t_venda['data_venda'], 'id_cliente': t_venda['id_cliente']}
sem_compras_90d1 = pd.DataFrame(data=sem_compras_90d).sort_index()

# Converter a coluna 'data' para o tipo datetime
sem_compras_90d1['data'] = pd.to_datetime(sem_compras_90d1['data'])

## Ordenar o banco pela data
sem_compras_90d1 = sem_compras_90d1.sort_values(by='data')

#data de referencia: ultima data de vendas - 2023-08-21
data_referencia = pd.Timestamp('2023-08-21')

# ultima data de compra de cada cliente
ultima_compra_por_cliente = sem_compras_90d1.groupby('id_cliente')['data'].max()

# data de referencia - ultima compra de cada cliente
diferenca_datas = data_referencia - ultima_compra_por_cliente

# filtrar clientes sem compras nos ultimos 90 dias
clientes_sem_compras = diferenca_datas[diferenca_datas > pd.Timedelta(days=90)]

# conversão para tabela
clientes_sem_compras_tab = pd.DataFrame(data=clientes_sem_compras).reset_index()

# quantidade de IDs de clientes sem compras nos últimos 90 dias
quantidade_clientes_sem_compras = len(clientes_sem_compras)

if st.checkbox('Clique aqui para abrir a tabela de clientes sem compras nos últimos 90 dias'):
    st.write(clientes_sem_compras_tab)   

st.write(f'A quantidade de contas sem compras a mais de 90 dias é {quantidade_clientes_sem_compras}.')

## PERCENTUAL DA QTD CONTAS SEM COMPRAS HÁ + DE 90 DIAS SOBRE A QTD CONTAS CADASTRADAS
st.subheader('Percentual da quantidade de contas sem compras há + de 90 dias sobre a quantidade de contas cadastradas')

perc_cadastradas_sc_90d = round(quantidade_clientes_sem_compras/contas_cadastradas *100, 2)

st.write(f'O percentual da quantidade de contas sem compras há + de 90 dias sobre a quantidade de contas cadastradas é {perc_cadastradas_sc_90d}%.')

## EVOLUÇÃO DAS CONTAS CADASTRADAS X ATIVADAS POR TRIMESTRE
st.subheader('Evolução das Contas Cadastradas x Ativadas por Trimestre')

### separar data e hora em colunas
t_cliente[['dt_cadastro1', 'hora_cadastro1']] = t_cliente['dt_cadastro'].str.split(' ', expand=True)

############ TRIMESTRE PARA CONTAS CADASTRADAS ###########
t_cliente['dt_cadastro1'] = pd.to_datetime(t_cliente['dt_cadastro1'])

# Função para determinar o trimestre
def trimestre(date):
    month = date.month
    if month >= 1 and month <= 3:
        return 1
    elif month >= 4 and month <= 6:
        return 2
    elif month >= 7 and month <= 9:
        return 3
    else:
        return 4

# Adicionar uma coluna para o trimestre
t_cliente['Trimestre'] = t_cliente['dt_cadastro1'].apply(lambda x: trimestre(x))

# unir as informações do trimestre
cadastradas_2018_a_2023 = t_cliente[(t_cliente['dt_cadastro1'].dt.year == 2023) | (t_cliente['dt_cadastro1'].dt.year == 2022) | (t_cliente['dt_cadastro1'].dt.year == 2021) | (t_cliente['dt_cadastro1'].dt.year == 2020) | (t_cliente['dt_cadastro1'].dt.year == 2019) | (t_cliente['dt_cadastro1'].dt.year == 2018)]


########### CADASTRADAS - AGRUPAR POR TRIMESTRE #########
cadastradas_trimestre = cadastradas_2018_a_2023.groupby('Trimestre').size()
cadastradas_trimestre = pd.DataFrame(data=cadastradas_trimestre).reset_index().rename(columns={'Trimestre': 'Trimestre', 0: 'Qtd'})

st.write("Cadastradas por Trimestre")

trimestre_cadastradas = px.bar(cadastradas_trimestre, x='Trimestre', y='Qtd', text_auto=True, color="Qtd")
st.plotly_chart(trimestre_cadastradas)

############ TRIMESTRE PARA CONTAS ATIVADAS ###########
# data de ativacao da conta
ativacao_conta = t_venda.groupby('id_cliente')['data_venda'].min()
ativacao_conta = pd.DataFrame(data=ativacao_conta).reset_index()

# coluna data para datetime
ativacao_conta['data_venda'] = pd.to_datetime(ativacao_conta['data_venda'])

# Função para determinar o trimestre
def trimestre(date):
    month = date.month
    if month >= 1 and month <= 3:
        return 1
    elif month >= 4 and month <= 6:
        return 2
    elif month >= 7 and month <= 9:
        return 3
    else:
        return 4

# Adicionar uma coluna para o trimestre
ativacao_conta['Trimestre'] = ativacao_conta['data_venda'].apply(lambda x: trimestre(x))

# Filtrar os dados para os anos 2020 e 2022
ativadas_2018_a_2023 = ativacao_conta[(ativacao_conta['data_venda'].dt.year == 2023) | (ativacao_conta['data_venda'].dt.year == 2022) | (ativacao_conta['data_venda'].dt.year == 2021) | (ativacao_conta['data_venda'].dt.year == 2020) | (ativacao_conta['data_venda'].dt.year == 2019) | (ativacao_conta['data_venda'].dt.year == 2018)]

########### ATIVADAS - AGRUPAR POR TRIMESTRE #########

ativadas_trimestre = ativadas_2018_a_2023.groupby('Trimestre').size()
ativadas_trimestre = pd.DataFrame(data=ativadas_trimestre).reset_index().rename(columns={'Trimestre': 'Trimestre',0: 'Qtd'})

st.write("Ativadas por Trimestre")

trimestre_ativadas = px.bar(ativadas_trimestre, x='Trimestre', y='Qtd', text_auto=True, color="Qtd")
st.plotly_chart(trimestre_ativadas)


########### EVOLUÇÃO DAS QTD CONTAS CADASTRADAS POR MÊS/ANO + ACUMULADO #######
st.subheader('Evolução das Qtd Contas Cadastradas por Mês/Ano + Acumulado')

# separar por ano e mês
t_cliente["ano_mês"] = t_cliente["dt_cadastro1"].dt.strftime('%Y-%m')

# qtd por ano e mês
ano_mes_agrupado = t_cliente.groupby('ano_mês').size()
ano_mes_agrupado = pd.DataFrame(data=ano_mes_agrupado).reset_index().rename(columns={'ano_mês': 'Ano_mes', 0: 'Qtd'})

# acumulado por mês e ano
ano_mes_agrupado_acumulado = ano_mes_agrupado['Qtd'].cumsum(axis=0)
ano_mes_agrupado_acumulado = pd.DataFrame(data=ano_mes_agrupado_acumulado).rename(columns={'Qtd': 'Acumulado'})

# concatenação das duas tabelas
contas_acumulado = pd.concat([ano_mes_agrupado, ano_mes_agrupado_acumulado], axis=1)

if st.checkbox('Clique aqui para abrir a tabela da evolução das contas cadastradas por mês/ano + acumulado'):
    st.write(contas_acumulado)  
    
# gráfico por mês e ano
grafico_ano_mes = px.bar(ano_mes_agrupado, x='Ano_mes', y='Qtd', text_auto=True, color="Qtd")

st.write("Contas cadastradas por mês/ano")

st.plotly_chart(grafico_ano_mes)

# gráfico acumulado 
st.write("Acumulado de contas cadastradas por mês/ano")

grafico_acumulado_ano_mes = px.bar(contas_acumulado, x='Ano_mes', y='Acumulado', text_auto=True, color="Acumulado")

st.plotly_chart(grafico_acumulado_ano_mes)

########### ATIVAÇÃO POR SAFRA #######
st.subheader('Ativação por Safra')

#ativacao_conta = t_venda.groupby('id_cliente')['data_venda'].min()
ativacao_conta = pd.DataFrame(data=ativacao_conta).reset_index()

#converter para datetime
ativacao_conta['data_venda'] = pd.to_datetime(ativacao_conta['data_venda'])

# separar por ano e mês
ativacao_conta['ano_mes'] = ativacao_conta["data_venda"].dt.strftime('%Y-%m')

# qtd por ano e mês
ano_mes_ativacao = ativacao_conta.groupby('ano_mes').size()
ano_mes_ativacao = pd.DataFrame(data=ano_mes_ativacao).reset_index().rename(columns={'ano_mes': 'Ano_mes', 0: 'Qtd'})

# gráfico qtd
grafico_ano_mes_ativacao = px.bar(ano_mes_ativacao, x='Ano_mes', y='Qtd', text_auto=True, color="Qtd")

st.plotly_chart(grafico_ano_mes_ativacao)