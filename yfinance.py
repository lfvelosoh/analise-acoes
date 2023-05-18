#realizando as importacoes necessarias
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import datetime
import os
import matplotlib.pyplot as plt
import glob

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

#recebendo dados da API

os.chdir("C:/Users/luis-/projetos/analise-acoes")
for i in range(len(df_acoes)): #cria um for utilizando a quantidade de acoes importadas na lista
    
    acao = yf.Ticker(df_acoes[i]) # atribuindo os dados da lista a variavel ticket, chamando o metodo Tickets
    df_busca = acao.history(period='12mo') #cria um dataframe para buscar os dados dos ultimos 5 anos

    #Verificando se a coluna acao ja existe no data frame
    aux = []
    if 'Acao' in df_busca.columns: #se coluna acao existir em Df_busca
        print("A coluna existe")
    else: #senão, preencher uma lista para adicionar uma nova coluna ao dataframe
        for f in range(len(df_busca)): #cria um for utilizando a quantidade de informacoes retornadas pela busca
            aux.append(df_acoes[i]) #adiciona o nome da acao em uma lista com a mesma qtde de itens que o DF possuir
        df_busca.insert(0,"Acao", aux, True) #adiciona a lista criada ao dataframe
    
    #Verificando se a data virou coluna e um novo indice foi criado
    if 'Date' in df_busca.columns:#se coluna data existir em Df_busca
        print("A coluna data ja existe")
    else: #Senão, converte o indice em uma coluna separada e cria um novo indice numerico
        df_busca.reset_index(inplace=True)#Convert index[Date] para data
    
    df_busca['Date'] = df_busca['Date'].dt.strftime('%Y-%m-%d') #Configura o formato da data para YY/mm/dd
    df_busca[['Date', 'Acao','Close', 'Dividends']].to_csv(str('./Database/'+df_acoes_orig[i]+'.csv')) #cria o arquivo com o nome da acao no caminho indicado
    print(str(df_acoes[i]) +" - Arquivo criado")

    df_busca['Date'] = pd.to_datetime(df_busca['Date']) #Converte o campo[Date] para datetime novamente

os.chdir("C:/Users/luis-/projetos/analise-acoes/Database")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ]) #combinar todos os arquivos da lista
combined_csv.to_csv( "C:/Users/luis-/projetos/analise-acoes/database.csv", index=False, encoding='utf-8-sig') #exportar para csv

os.chdir("C:/Users/luis-/projetos/analise-acoes/")
df_database = pd.read_csv("./database.csv", sep = ',') #importando dados de um csv utilizando o pandas
pd.options.display.float_format = '${:,.2f}'.format
print(df_database[['Date', 'Acao','Close', 'Dividends']].query('Dividends > 0'))


df_dy = df_database[['Date', 'Acao','Close', 'Dividends']].query('Dividends > 0')
df_dy['DY'] = (df_dy.Dividends / df_dy.Close)*100
pd.options.display.float_format = '{:,.2f}%'.format
print(df_dy[['Date', 'Acao', 'DY']])

#criar os graficos
x='Date'
y='DY'
teste = df_dy.plot.bar(x,y, 
                       figsize=(25,3), 
                       title='Dividend Yeild last 12 months from '+str(df_dy['Acao'].iloc[0]))
