import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import tabulate



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
st.bar_chart(data=t_cliente['fl_status_conta'].value_counts(), color='#81689D')

st.text(f'O percentual de contas bloqueadas em relação às contas cadastradas {bloqueadas_cadastradas:.2f}%.')

## QTD/PERCENTUAL DE CONTAS POR SITUAÇÃO ##
st.subheader('Quantidade/Percentual de Contas por Situação')

contas_situacao = t_cliente.groupby(['fl_status_conta']).size().reset_index().rename(columns={'fl_status_conta': 'Status',0: 'Contas'})

if st.checkbox('Clique aqui para abrir as contas por situação'):
    st.write(contas_situacao) 
    
st.bar_chart(data=contas_situacao, x= 'Status', y='Contas', color='#81689D') 

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

st.bar_chart(data=contas_origem, x='Origem', y='Qtd', color='#81689D')

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

st.bar_chart(data=cartoes_situacao, x= 'Status', y='Qtd', color='#81689D')    

## QTD CARTÕES POR TIPO DE BLOQUEIO ##
st.subheader('Quantidade de Cartões por Tipo de Bloqueio')
t_bloqueio_cartao = pd.read_csv('t_bloqueio_cartao_202402071704.csv')
cartoes_bloqueio = t_bloqueio_cartao.groupby('id_tipo_bloqueio_cartao')['id_cartao'].nunique().reset_index().rename(columns={'id_tipo_bloqueio_cartao': 'Tipo de Bloqueio', 'id_cartao': 'Qtd'})

if st.checkbox('Clique aqui para abrir a tabela de cartões-bloqueio'):
    st.write(cartoes_bloqueio)
    
st.bar_chart(data=cartoes_bloqueio, x= 'Tipo de Bloqueio', y='Qtd', color='#81689D') 

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
    
