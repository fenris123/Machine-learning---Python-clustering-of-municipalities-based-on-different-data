"""
Script de extracción y transformación de datos municipales.

Estructura de directorios esperada:

Proyecto/
│
├─ Entrada/                <- Carpeta donde se colocan los archivos de datos
│   ├─ censo municipal 2021-2025.csv
│   ├─ renta media por hogar.csv
│   ├─ DensPob2023.shp
│   └─ NumParados_2022.shp
│
└─ este_script.py          <- Script que realiza la transformación

Descripción:

1. PASO 1: Carga y limpieza del censo municipal 2021-2025.
   - Filtra solo filas de "Sexo" Total y Periodos 2021 y 2025.
   - Separa columna 'Municipios' en 'Código municipal' y 'Municipio'.
   - Calcula la variación porcentual de población.

2. PASO 2: Carga y limpieza de la renta media por hogar.
   - Filtra el periodo 2023 y el indicador "Renta neta media por persona".
   - Limpia los valores numéricos eliminando separadores de miles y convirtiendo coma a punto decimal.
   - Calcula la media por municipio.

3. PASO 3: Extracción de densidad de población desde shapefile.
   - Crea un DataFrame con columnas 'Código municipal', 'Municipio' y 'Densidad de población'.

4. PASO 4: Extracción de parados por 1000 personas desde shapefile.
   - Crea un DataFrame con columnas 'Código municipal', 'Municipio' y 'Parados por 1000'.

5. PASO 5: Unión de todos los DataFrames en uno solo.
   - Realiza inner join usando 'Código municipal' para asegurar consistencia.
   - Elimina automáticamente códigos no coincidentes.

6. PASO FINAL: Exportación del DataFrame final a CSV.
"""







import os
import pandas as pd
import geopandas as gpd


# PASO 0:  establecer el directorio donde esta el script, y dentro de el la carpeta donde estaran los datos
base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Entrada")



#  PASO 1:  CARGA Y LIMPIEZA DE ARCHIVO CENSO MUNICIPAL 2021-2025

archivo_censo = os.path.join(entrada_dir, "censo municipal 2021-2025.csv")

try:
    df_censo = pd.read_csv(archivo_censo, encoding='utf-8', sep=";")  # prueba con utf-8
except UnicodeDecodeError:
    df_censo = pd.read_csv(archivo_censo, encoding='latin1',sep =";")  # fallback si hay acentos



# Eliminamos filas donde Municipios es NaN
df_censo = df_censo.dropna(subset=["Municipios"])

# Filtramos filas donde Sexo sea "Total"
df_censo = df_censo[df_censo["Sexo"] == "Total"]

# Filtramos filas donde Periodo sea 2021 o 2025
df_censo = df_censo[df_censo["Periodo"].isin([2021, 2025])]

# Separamos la columna "Municipios" en código y nombre
df_censo[["Código municipal", "Municipio"]] = df_censo["Municipios"].str.split(" ", n=1, expand=True)

# Quitamos columnas innecesarias
df_censo = df_censo.drop(columns=["Total Nacional","Sexo", "Municipios"])


# despivotar la fila del periodo a columnas.
df_censo = df_censo.pivot(
    index=["Código municipal", "Municipio"],
    columns="Periodo",
    values="Total"
).reset_index()


df_censo = df_censo.rename(columns={
    2021: "Población 2021",
    2025: "Población 2025"
})


# Quitamos los puntos de miles, y convertimos a numerico
df_censo["Población 2021"] = df_censo["Población 2021"].str.replace(".", "", regex=False)
df_censo["Población 2025"] = df_censo["Población 2025"].str.replace(".", "", regex=False)

# Convertimos a numérico
df_censo["Población 2021"] = pd.to_numeric(df_censo["Población 2021"], errors="coerce")
df_censo["Población 2025"] = pd.to_numeric(df_censo["Población 2025"], errors="coerce")


# Columna de variacion de población.
df_censo["Variación % población"] = (
    (df_censo["Población 2025"] - df_censo["Población 2021"])
    / df_censo["Población 2021"].replace(0, pd.NA)
) * 100








#  PASO 2:  CARGA Y LIMPIEZA DE ARCHIVO RENTA MEDIA POR HOGAR


archivo_renta = os.path.join(entrada_dir, "renta media por hogar.csv")

try:
    df_renta = pd.read_csv(archivo_renta, encoding='utf-8', sep=";")
except UnicodeDecodeError:
    df_renta = pd.read_csv(archivo_renta, encoding='latin1', sep=";")



# Filtramos filas donde Periodo sea 2023
df_renta = df_renta[df_renta["Periodo"] == 2023]

# Filtramos filas donde el indicador sea la renta por persona y renombramos Total
df_renta = df_renta[df_renta["Indicadores de renta media"] == "Renta neta media por persona"]
df_renta = df_renta.rename(columns={"Total": "Renta neta media por persona"})


# Quitamos los puntos de miles, y convertimos a numerico.  Valores no válidos pasan a NaN
df_renta["Renta neta media por persona"] = (
    df_renta["Renta neta media por persona"]
    .str.replace(".", "", regex=False)  # quitamos separador de miles
    .str.replace(",", ".", regex=False)  # convertimos coma decimal a punto
)

df_renta["Renta neta media por persona"] = pd.to_numeric(
    df_renta["Renta neta media por persona"], errors="coerce"
)


# Separamos la columna "Municipios" en código y nombre
df_renta[["Código municipal", "Municipio"]] = df_renta["Municipios"].str.split(" ", n=1, expand=True)

# Quitamos columnas innecesarias
df_renta = df_renta.drop(columns=["Municipios", "Distritos", "Secciones","Indicadores de renta media", "Periodo"])

#  Sacamos la media de los valores de renta media de cada municipio cada municipio (habia varios valores, uno para cada seccion, etc)
df_renta = (
    df_renta
    .groupby(["Código municipal", "Municipio"], as_index=False)
    ["Renta neta media por persona"]
    .mean()
)




# PASO 3:  extraer los datos de densidad de poblacion del archivo shp.

archivo_shp = os.path.join(entrada_dir, "DensPob2023.shp")

gdf = gpd.read_file(archivo_shp)

# Crear df_densidad con solo las columnas necesarias
df_densidad = gdf[["nombre", "codmun_ine", "dens_pob"]].copy()

# Renombrar columnas para mayor claridad
df_densidad = df_densidad.rename(columns={
    "nombre": "Municipio",
    "codmun_ine": "Código municipal",
    "dens_pob": "Densidad de población"
})

del gdf



# PASO 4:  extraer los datos de parados por cada 1000 personas del archivo shp.


archivo_shp = os.path.join(entrada_dir, "NumParados_2022.shp")

gdf = gpd.read_file(archivo_shp)


# Crear df_parados con solo las columnas necesarias
df_parados = gdf[["nombre", "codmun_ine", "paro_1000"]]

# Renombrar columnas para mayor claridad
df_parados = df_parados.rename(columns={
    "nombre": "Municipio",
    "codmun_ine": "Código municipal",
    "paro_1000": "Parados por 1000"
})

del gdf



# Paso 5: Crear un unico df con todos los datos.



df_final = df_censo.copy()

# Eliminamos la columna "Municipio" de los demás df para evitar conflictos al hacer merge
df_renta_sin_nombre = df_renta.drop(columns="Municipio")
df_densidad_sin_nombre = df_densidad.drop(columns="Municipio")
df_parados_sin_nombre = df_parados.drop(columns="Municipio")

# Merge sucesivos usando inner join sobre 'Código municipal'
df_final = df_final.merge(df_renta_sin_nombre, on="Código municipal", how="inner")
df_final = df_final.merge(df_densidad_sin_nombre, on="Código municipal", how="inner")
df_final = df_final.merge(df_parados_sin_nombre, on="Código municipal", how="inner")

# Comprobar si el número de filas coincide con lo esperado
print(f"Número de municipios tras el merge: {len(df_final)}")



# PASO FINAL:  Sacamos el archivo a csv
df_final.to_csv(os.path.join(base_dir, "Intermedio/f_municipios_completo.csv"), index=False, sep=";")
