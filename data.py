from datetime import datetime
import functions as funct
inversion_inicial = 1000000
comision = 0.00125
start = datetime.strptime("2020-01-31", '%Y-%m-%d')
end = datetime.strptime("2022-01-26", '%Y-%m-%d')

ponderaciones = funct.csv_cleaner('20200131')
stock_dataYF = funct.yahoo_download(ponderaciones,start,end)
titulos = funct.pond(ponderaciones, stock_dataYF, inversion_inicial, comision)

qqq = funct.stock('QQQ',start,end)
qqq = funct.medidas_des(qqq,0,'QQQ')
arkk = funct.stock('ARKK',start,end)
arkk = funct.medidas_des(arkk,0,'ARKK')

voo =funct.stock('VOO',start,end)
voo = funct.medidas_des(voo,0,'S&P 500')