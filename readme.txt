This is a proyect to make a ML proyect to clustering the spanish municipalities acording to data related to them.


Por motivos didacticos se ha dejado el script de cada paso por separado, para ir ejecutando uno por uno

El orden es preparacion_datos, histograma y correlacion_variables, analisis_codo, algoritmo_agrupacion  y visualizacion


1- FUENTES DE DATOS Y TRANSFORMACIONES REALIZADAS A ESAS FUENTES DE DATOS.

Todas estas transformaciones para preparar nuestros datos seran realizadas por el script Preparacion_datos.py, que nos devolvera un .csv
Ese .csv ya estara listo para iniciar el proceso de agrupacion.
Es posible que el proceso de agrupacion requiera  alguna transformación adicional para realizarse.
En este proceso solo hemos querido incluir la preparacion basica de los datos desde varias fuentes a un solo archivo.  
Operaciones como un posible análisis de componentes principales por ejemplo, aunque sean en puridad transformaciones, tienen mas sentido en pasos posteriores.

FUENTES.
1- Spanish census data 2021-2025
  Source: https://www.ine.es/jaxiT3/Tabla.htm?t=68065

2- Renta media por hogar.
  Source: https://www.ine.es/dynt3/inebase/index.htm?padre=12385&capsel=12384

3- Densidad de poblacion (hay que sacarla de un archivo shp)
  Source: https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/reto-demografico/datos-demograficos.html
  Fuente: «© Ministerio para la Transición Ecológica y el Reto Demográfico»

4- Numero de parados por cada 1000 habitantes diciembre 2022. (hay que sacarla de un archivo shp)
    Source https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/reto-demografico/datos-economicos.html
     Fuente: «© Ministerio para la Transición Ecológica y el Reto Demográfico»

The data where retrieved in 17/03/2026


Transformaciones:

  Spanish census data 2021-2025
  Se eliminan filas donde la columna Municipios está vacía.
  Se filtran filas para conservar únicamente aquellas donde Sexo es "Total" y el Periodo es 2021 o 2025.
  La columna Municipios se divide en dos: Código municipal (el código) y Municipio (el nombre).
  Se eliminan las columnas Total Nacional, Sexo y la columna original Municipios por no aportar información relevante.
  Se despivotan los valores de Periodo para que 2021 y 2025 sean columnas independientes (Población 2021 y Población 2025).
  Se limpian los valores de población eliminando los puntos usados como separador de miles y se convierten a numérico.
  Se calcula la columna Variación % población, indicando el porcentaje de cambio entre 2021 y 2025.

  
  Renta media por hogar
  Se filtran filas para conservar únicamente aquellas donde el Periodo es 2023.
  Se filtran filas para conservar únicamente aquellas cuyo indicador es "Renta neta media por persona".
  La columna Municipios se divide en dos: Código municipal (el código) y Municipio (el nombre).
  Se eliminan las columnas Municipios, Distritos, Secciones, Indicadores de renta media y Periodo por no aportar información relevante.
  Se limpian los valores de renta eliminando los puntos de miles y convirtiendo la coma decimal a punto.
  Se convierten los valores de renta a numérico, asignando NaN en caso de valores no válidos.
  Se agrupan los registros por municipio (Código municipal y Municipio) y se calcula la renta media por persona como promedio de los valores disponibles por  municipio.
  Se eliminan los municipios con renta media no disponible.  (73 municipios con un maximo de poblaccion de 116 personas. No afectara mucho al analisis. Simplemente se podrian llegar a considerar un grupo propio a la hora de representarlos en un mapa)


  Densidad de población 2023
  Se carga el shapefile "DensPob2023.shp" usando geopandas.
  Se extraen únicamente las columnas necesarias: nombre del municipio, código municipal y densidad de población.
  Se renombraron las columnas a: "Municipio", "Código municipal" y "Densidad de población" para mayor claridad y coherencia con los anteriores.
  Se eliminó el GeoDataFrame original para liberar memoria.



  Parados por cada 1000 personas
  Se carga el shapefile "NumParados_2022.shp" usando geopandas.
  Se extraen únicamente las columnas necesarias: nombre del municipio, código municipal y Parados por 1000.
  Se renombraron las columnas a: "Municipio", "Código municipal" y "Parados por 1000" para mayor claridad y coherencia con los anteriores.
  Se eliminó el GeoDataFrame original para liberar memoria.




Finalmente se unen todos esos datos en un solo df. El join se realizara por el codigo municipal.  El nombre del municipio se tomara el presente en los datos del censo.

IMPORTANTE:  Hay 8 municipios que aparecen solo en 2 de los listados iniciales.  Se ha optado por directamente eliminarlos.


2 PRIMER ANALISIS DE LAS VARIABLES MEDIANTE UN HISTOGRAMA.

Se procede a representar un histograma de las diferentes variables.  Encontramos que Poblacion y Densidad de Poblacion estan demasiado agrupadas, habiendo por ejemplo muchisimos municipios pequeños y muy pocos grandes que son invisibles, por lo que añadimos una representacion logaritmica para esas dos variables durante el analisis.


3 COMPROBACION DE EXISTENCIA O NO DE CORRELACIÓN ENTRE VARIABLES.

Comprobamos la existencia o no de correlacion entre las variables que hemos tomado para hacer el analisis. (poblacion 2025, variacion de la poblacion entre 2021 y 2025, renta media por persona, densidad de poblacion, y parados por cada mil.

Hay una correlacion de 0.31 y otra de 0.48. El resto esta por debajo de 0.1 asi que consideramos que (sobre todo para un proyecto personal) la independencia de las variables es mas que suficiente y no merece la pena hacer un analisis de componente principales.


4 DETERMINACION DEL NUMERO OPTIMO DE GRUPOS MEDIANTE LA TECNICA DEL CODO.

Se elige un numero de grupos de 10.

5 EJECUCION DEL ALGORITMO DE AGRUPACION.

incluye normalizacion de las variables.

6  VISUALIZACION DE LOS DATOS EN UN MAPA SHP.

Se ha eliminado canarias por problema de tamaño para incluirlo todo en una sola imagen.  Se puede crear una representacion para ella sola.



