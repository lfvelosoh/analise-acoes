#realizando as importacoes necessarias
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import datetime

#realizando override para trabalhar com o pandas_datareader
yf.pdr_override()

#definindo data de inicio e fim, caso necessario
start = '2020-01-01'
end = '2023-03-01'