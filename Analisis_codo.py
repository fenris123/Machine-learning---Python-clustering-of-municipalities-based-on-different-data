# pip install pandas matplotlib scikit-learn
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler   # <-- AÑADIDO

# --- Carga de datos ---
base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Intermedio")
archivo_municipios = os.path.join(entrada_dir, "f_municipios_completo.csv")

try:
    df = pd.read_csv(archivo_municipios, encoding='utf-8', sep=";")
except UnicodeDecodeError:
    df = pd.read_csv(archivo_municipios, encoding='latin1', sep=";")

# --- Filtrar ---
df_cluster = df[(df['Población 2025'] > 0) & (df['Densidad de población'] > 0)].copy()

# --- Log ---
df_cluster['Población 2025'] = np.log(df_cluster['Población 2025'])
df_cluster['Densidad de población'] = np.log(df_cluster['Densidad de población'])

# --- Variables ---
columnas = [
    'Población 2025',
    'Variación % población',
    'Renta neta media por persona',
    'Densidad de población',
    'Parados por 1000'
]

# --- Eliminar NaN ---
df_cluster = df_cluster.dropna(subset=columnas)

X = df_cluster[columnas]

# --- NORMALIZACIÓN ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


wcss = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# --- Gráfico del codo ---
plt.figure(figsize=(8,5))
plt.plot(k_range, wcss, marker='o')
plt.xlabel('Número de clusters (k)')
plt.ylabel('WCSS (inercia)')
plt.title('Técnica del codo (datos normalizados)')
plt.grid(True)
plt.show()


kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
df_cluster['Cluster'] = kmeans.fit_predict(X_scaled)



pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# --- Gráfico ---
plt.figure(figsize=(10,6))
scatter = plt.scatter(
    X_pca[:,0],
    X_pca[:,1],
    c=df_cluster['Cluster'],
    cmap='tab10',
    alpha=0.3
)
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.title('Clusters de municipios (K-Means, 10 grupos) - PCA')
plt.colorbar(scatter, label='Cluster')
plt.grid(True)
plt.show()
