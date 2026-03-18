# pip install pandas
import os
import pandas as pd


#  PASO 1:  CARGA Y LIMPIEZA DE ARCHIVO CENSO MUNICIPAL 2021-2025


base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Entrada")
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


# Antes de convertir a numérico, quitamos los puntos de miles
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


base_dir = os.path.dirname(os.path.abspath(__file__))
entrada_dir = os.path.join(base_dir, "Entrada")
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


# Limpiar la columna de renta
df_renta["Renta neta media por persona"] = (
    df_renta["Renta neta media por persona"]
    .str.replace(".", "", regex=False)  # quitamos separador de miles
    .str.replace(",", ".", regex=False)  # convertimos coma decimal a punto
)

# Convertimos a numérico, valores no válidos pasan a NaN
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

