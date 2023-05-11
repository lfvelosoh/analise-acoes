#realizando as importacoes necessarias
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import datetime
import os

#realizando override para trabalhar com o pandas_datareader
yf.pdr_override()

#definindo data de inicio e fim, caso necessario
start = '2020-01-01'
end = '2023-03-01'

#importando a lista de acoes

os.chdir("C:/Users/luis-/projetos/analise-acoes") #selecionando o diretorio do arquivo CSV a ser lido
df_acoes = pd.read_csv("./Tickets.csv", sep = ',') #importando dados de um csv utilizando o pandas
df_acoes_orig = df_acoes.copy() #Criando uma copia original dos dados antes da alteracao
df_acoes['Ativo'] = df_acoes['Ativo'].map('{}.SA'.format) #concatenando o sufixo '.sa' na coluna Ativo, para pesquisa
df_acoes = df_acoes['Ativo'].tolist() #convertendo o data frame para lista
df_acoes_orig = df_acoes_orig['Ativo'].tolist() #Criando uma copia original dos dados antes da alteracao