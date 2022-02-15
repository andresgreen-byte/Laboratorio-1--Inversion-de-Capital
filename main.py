from operator import inv
import functions as funct
import data as dt
from datetime import datetime
import plotly.express as px

inversion_inicial = 1000000
comision = 0.00125
rf = 0.0575/12
start = datetime.strptime("2020-01-31", '%Y-%m-%d')
end = datetime.strptime("2022-01-26", '%Y-%m-%d')

inversion_pasiva = funct.passive_investment(dt.ponderaciones,dt.stock_dataYF,inversion_inicial,comision)
print(inversion_pasiva.tail(5))
medid_pasiva = funct.medidas_des(inversion_pasiva,rf,'Pasiva')
print(medid_pasiva)

inversion_pasiva = inversion_pasiva.set_index('Date')
fig = px.line(inversion_pasiva,y=inversion_pasiva['Capital'],title='Capital Inversión Pasiva',)
fig.show()