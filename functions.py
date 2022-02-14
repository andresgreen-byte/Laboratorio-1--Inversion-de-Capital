import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import functions as funct

def csv_cleaner(date): #
    df = pd.read_csv('C:/Users/ii713/Documents/GitHub/Laboratorio-1--Inversion-de-Capital/files/NAFTRAC_'+date+'.csv',header=2)
    df = df[:-1]
    df['Ticker'] = df['Ticker'].str.replace('*', '')
    df['Ticker'] = df['Ticker'].replace('LIVEPOLC.1', 'LIVEPOLC-1')
    df['Ticker'] = df['Ticker'].astype(str) + '.MX'
    replace_tickers = ["KOFL.MX", "KOFUBL.MX", "USD.MXN", "BSMXB.MX", "NMKA.MX"]
    df['Ticker'] = df['Ticker'].replace(replace_tickers, 'MXN.MX')
    df= pd.concat([df[['Ticker','Peso (%)']]]).groupby('Ticker',as_index = False)[
    'Peso (%)'].sum()
    date = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    df['Date'] = date
    df = df[["Ticker","Peso (%)","Date"]]
    return df.fillna(0)

def yahoo_download(df,start,end):
    df = df['Ticker'].unique()
    tickers = df.tolist()
    prices = yf.download(tickers, start=start, end=end)
    prices = prices['Adj Close']
    prices = prices.reset_index()
    prices['Date'] = pd.to_datetime(prices['Date'])
    prices = prices.set_index('Date') 
    prices = prices.groupby(pd.Grouper(freq='M')).tail(1)
    return prices.fillna(0)

def passive_investment(ponderaciones, stock_dataYF, inversion_inicial, comision):
    pond = ponderaciones.pivot(index='Date',columns='Ticker', values='Peso (%)')
    pond.iloc[0] = pond.iloc[0]/100
    pond= pd.concat([pond,stock_dataYF],axis=0)
    pond = pond.head(2)
    pond.loc['Monto Inicial']=((pond.iloc[0]*inversion_inicial))
    cash = pond['MXN.MX'].iloc[2]
    pond.loc['Títulos'] = round(pond.iloc[2].div(pond.iloc[1]),0)
    pond.loc['Monto Comprado'] = pond.iloc[3]*pond.iloc[1]
    cost_trans = pond.iloc[4].sum(axis=0)*comision
    cash = cash-cost_trans
    rendimientos = stock_dataYF*pond.iloc[3]
    rendimientos['Capital'] = rendimientos.sum(axis=1)+cash
    rendimientos['Rendimiento'] = rendimientos['Capital'].pct_change()
    rendimientos['Rend Acumulado'] = rendimientos['Rendimiento'].cumsum()
    rendimientos = rendimientos.reset_index()
    rendimiento_PASIVA = rendimientos[['Date','Capital','Rendimiento','Rend Acumulado']].fillna(0)
    return rendimiento_PASIVA

def medidas_des(inversion,rf,estrategia):
    sr = ((inversion['Rendimiento'].mean()-rf)/inversion['Rendimiento'].std())*(12)**(0.5)
    rp = inversion['Rendimiento'].mean()
    ra = inversion['Rendimiento'].sum()
    df = pd.DataFrame({'Medida':['Rendimiento Promedio Mensual','Rendimiento Mensual Acumulado','Sharpe Ratio'],estrategia:[rp,ra,sr]})
    df = df.set_index('Medida')
    return df
