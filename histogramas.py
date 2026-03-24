# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 2026

@author: fenris123

Histogramas de columnas numéricas de municipios:
- Lineales para todas las columnas
- Logarítmicos para Población y Densidad (en unidades reales)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Intermedio")
archivo_municipios = os.path.join(entrada_dir, "f_municipios_completo.csv")

try:
    df= pd.read_csv(archivo_municipios, encoding='utf-8', sep=";")  # prueba con utf-8
except UnicodeDecodeError:
    df= pd.read_csv(archivo_municipios, encoding='latin1',sep =";")  # fallback si hay acentos

# Columnas a graficar
cols_numericas = [
    'Población 2025',
    'Variación % población',
    'Renta neta media por persona',
    'Densidad de población',
    'Parados por 1000'
]

# Columnas para escala log
cols_log = ['Población 2025', 'Densidad de población']

# Histograma lineal para todas las columnas
for col in cols_numericas:
    plt.figure(figsize=(8,5))
    sns.histplot(df[col], bins=30, color='steelblue', kde=True, stat="count")

    # Ajustar eje X al rango de datos
    margen = 0.05 * (df[col].max() - df[col].min())
    plt.xlim(df[col].min() - margen, df[col].max() + margen)

    plt.title(f'Histograma lineal de {col}', fontsize=14)
    plt.xlabel(col, fontsize=12)
    plt.ylabel('Número de municipios', fontsize=12)
    plt.grid(axis='y', alpha=0.75)
    plt.show()

# Histograma logarítmico para columnas seleccionadas
for col in cols_log:
    data = df[col]

    # Crear bins logarítmicos desde mínimo hasta máximo real
    bins_log = np.logspace(np.log10(data.min()), np.log10(data.max()), 30)

    plt.figure(figsize=(8,5))
    plt.hist(data, bins=bins_log, color='orange', edgecolor='black')
    plt.xscale('log')

    plt.xlabel(f'{col} (log)', fontsize=12)
    plt.ylabel('Número de municipios', fontsize=12)
    plt.title(f'Histograma logarítmico de {col}', fontsize=14)
    plt.grid(axis='y', alpha=0.75, which='both')

    # Limitar eje X exactamente al rango de datos
    plt.xlim(data.min(), data.max())

    plt.show()
