import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# --- Carga de datos ---
base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Intermedio")
archivo_municipios = os.path.join(entrada_dir, "f_municipios_completo.csv")

try:
    df = pd.read_csv(archivo_municipios, encoding='utf-8', sep=";")
except UnicodeDecodeError:
    df = pd.read_csv(archivo_municipios, encoding='latin1', sep=";")


# --- Filtrar filas con Población 2025 y Densidad > 0 para poder aplicar log ---
df_cluster = df[(df['Población 2025'] > 0) & (df['Densidad de población'] > 0)].copy()

# --- Aplicar logaritmo natural a Población 2025 y Densidad de población ---
df_cluster['Población 2025'] = np.log(df_cluster['Población 2025'])
df_cluster['Densidad de población'] = np.log(df_cluster['Densidad de población'])

# --- Selección de columnas para clustering (sin Código municipal) ---
X = df_cluster[
    ['Población 2025', 'Variación % población', 'Renta neta media por persona',
     'Densidad de población', 'Parados por 1000']
]



# --- Técnica del codo ---
wcss = []
k_range = range(1, 15)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# --- Gráfico del codo ---
plt.figure(figsize=(8,5))
plt.plot(k_range, wcss, marker='o')
plt.xlabel('Número de clusters (k)')
plt.ylabel('WCSS')
plt.title('Técnica del codo')
plt.grid(True)
plt.show()