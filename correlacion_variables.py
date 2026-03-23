# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:34:35 2026

@author: fenris123
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ruta_csv = r"W:\espaciopython\proyecto_ml_municipios\Intermedio\f_municipios_completo.csv"
df = pd.read_csv(ruta_csv, sep=';')  # separador correcto

# Seleccionar solo las columnas numéricas que quieres analizar
cols_numericas = [
    'Población 2025',
    'Variación % población',
    'Renta neta media por persona',
    'Densidad de población',
    'Parados por 1000'
]

df_num = df[cols_numericas]

# Información general y estadísticas
print(df_num.info())
print(df_num.describe())


# Mapa de calor de correlaciones
plt.figure(figsize=(10,8))
sns.heatmap(df_num.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.show()
