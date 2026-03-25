# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:34:35 2026

@author: fenris123
"""

# pip install pandas matplotlib seaborn

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Rutas dinámicas ---
base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Intermedio")
archivo_csv = os.path.join(entrada_dir, "f_municipios_completo.csv")

# --- Cargar datos ---
df = pd.read_csv(archivo_csv, sep=';')

# --- Columnas numéricas ---
cols_numericas = [
    'Población 2025',
    'Variación % población',
    'Renta neta media por persona',
    'Densidad de población',
    'Parados por 1000'
]

df_num = df[cols_numericas]

# --- Mapa de calor ---
plt.figure(figsize=(10,8))
sns.heatmap(df_num.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Matriz de correlación")
plt.show()
