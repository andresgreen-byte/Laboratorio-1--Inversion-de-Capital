from operator import inv
import functions as funct
import data as dt
from datetime import datetime

inversion_inicial = 1000000
comision = 0.00125
rf = 0.0575/12

inversion_pasiva = funct.passive_investment(dt.ponderaciones,dt.stock_dataYF,inversion_inicial,comision)
print(inversion_pasiva.tail(5))
medid_pasiva = funct.medidas_des(inversion_pasiva,rf,'Pasiva')
print(medid_pasiva)