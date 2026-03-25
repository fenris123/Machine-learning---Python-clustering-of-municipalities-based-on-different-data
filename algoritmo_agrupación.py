# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:53:22 2026

@author: fenris123
"""

# pip install pandas matplotlib scikit-learn
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# --- Carga de datos ---
base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Intermedio")
archivo_municipios = os.path.join(entrada_dir, "f_municipios_completo.csv")

try:
    df = pd.read_csv(archivo_municipios, encoding='utf-8', sep=";")
except UnicodeDecodeError:
    df = pd.read_csv(archivo_municipios, encoding='latin1', sep=";")

# --- Filtrar filas con Población 2025 y Densidad > 0 para poder aplicar log ---
#  (opcional en nuestro dataset, porque ya hemos comprobado esos datos antes, lo mantenemos por seguridad)
df_cluster = df[(df['Población 2025'] > 0) & (df['Densidad de población'] > 0)].copy()

# --- Aplicar logaritmo natural a Población 2025 y Densidad de población ---
df_cluster['Población 2025'] = np.log(df_cluster['Población 2025'])
df_cluster['Densidad de población'] = np.log(df_cluster['Densidad de población'])

# --- Selección de columnas para clustering (sin Código municipal) ---
X = df_cluster[
    ['Población 2025', 'Variación % población', 'Renta neta media por persona',
     'Densidad de población', 'Parados por 1000']
]

# --- K-Means con 10 clusters ---
kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
df_cluster['Cluster'] = kmeans.fit_predict(X)

# --- Reducción de dimensionalidad con PCA para visualización ---
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# --- Crear gráfico ---
plt.figure(figsize=(10,6))
scatter = plt.scatter(X_pca[:,0], X_pca[:,1], c=df_cluster['Cluster'], cmap='tab10', alpha=0.3)
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.title('Clusters de municipios (K-Means, 10 grupos) - Proyección PCA')
plt.colorbar(scatter, label='Cluster')
plt.grid(True)
plt.show()


# --- Guardar el DataFrame con los clusters en la carpeta Intermedio ---
resultado_dir = os.path.join(base_dir, "Intermedio")
resultado_csv = os.path.join(resultado_dir, "municipios_clusterizados.csv")

df_cluster.to_csv(resultado_csv, index=False, sep=";")
print(f"Archivo guardado en: {resultado_csv}")
