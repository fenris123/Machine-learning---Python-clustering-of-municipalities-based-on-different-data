import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.cm import get_cmap
import contextily as ctx

# --- Leer shapefile con geometrías ---
base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Entrada")
salida_dir = os.path.join(base_dir, "Salida")
archivo_shp = os.path.join(entrada_dir, "DensPob2023.shp")
gdf = gpd.read_file(archivo_shp)

# --- Leer CSV con clusters ---
archivo_clusters = os.path.join(base_dir, "Intermedio", "municipios_clusterizados.csv")
df_clusters = pd.read_csv(archivo_clusters, encoding='utf-8', sep=';')

# --- Preparar merge ---
gdf['codmun_ine'] = gdf['codmun_ine'].astype(int)
df_clusters['Código municipal'] = df_clusters['Código municipal'].astype(int)

gdf = gdf.merge(
    df_clusters[['Código municipal', 'Cluster']],
    left_on='codmun_ine',
    right_on='Código municipal',
    how='left'
)

gdf['Cluster'] = gdf['Cluster'].fillna(99).astype(int)

# --- Reproyectar a Web Mercator (EPSG:3857) ---
gdf_web = gdf.to_crs(epsg=3857)

# Convertir Cluster a categoría
gdf_web['Cluster'] = gdf_web['Cluster'].astype('category')

# Quitar Canarias
gdf_web = gdf_web[~gdf_web['codmun_ine'].astype(str).str.startswith(('35', '38'))]



colores_clusters = [
    "#1f77b4",  # azul
    "#ff7f0e",  # naranja
    "#2ca02c",  # verde
    "#d62728",  # rojo
    "#9467bd",  # morado
    "#8c564b",  # marrón
    "#e377c2",  # rosa
    "#7f7f7f",  # gris
    "#bcbd22",  # lima
    "#17becf"   # cian
]

clusters = sorted(gdf_web['Cluster'].cat.categories)
cluster_colors = {c: colores_clusters[i] if c != 99 else "white" for i, c in enumerate(clusters)}




# --- Crear figura ---
fig, ax = plt.subplots(figsize=(30, 30))

# Plot usando esos colores
gdf_web.plot(
    color=gdf_web['Cluster'].map(cluster_colors),
    linewidth=0.2,
    edgecolor='white',
    alpha=0.7,
    ax=ax
)


# --- Añadir mapa base ---
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)



# --- Crear parches para la leyenda ---
patches = [
    mpatches.Patch(
        color=cluster_colors[c],
        label='Sin datos' if c == 99 else f'Cluster {c}'
    )
    for c in clusters
]

ax.legend(handles=patches, fontsize=18, loc='lower left', title='Clusters', title_fontsize=20)

# --- Guardar como JPG ---
archivo_salida = os.path.join(salida_dir, "municipios_clusters.jpg")
plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
print(f"Mapa guardado en: {archivo_salida}")

plt.show()