from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re
import requests
import json


base="dark"

def eliminar_numeros_caracteres(texto):
    # Definir la expresión regular para eliminar números y caracteres especiales
    patron = r'[^a-zA-Z\s]'

    # Utilizar re.sub() para eliminar los números y caracteres especiales
    texto_procesado = re.sub(patron, '', str(texto))

    return texto_procesado

def buscar_img(movie_id):
    api_key = "a3409f83d17ab83dbed7e4622bf4dbf2"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    response = requests.get(url)
    if response.status_code == 200:
        movie_data = json.loads(response.content)
        if movie_data.get("poster_path"):
            poster_path = movie_data["poster_path"]
            image_url = f"https://image.tmdb.org/t/p/original/{poster_path}"
            return image_url
def recomendacion(pelicula):
    # Convertir la columna "popularidad" a tipo numérico
    peliculas["popularidad"] = peliculas["popularidad"].astype(float)

    vectores = TfidfVectorizer(ngram_range=(1, 2))
    tfidf = vectores.fit_transform(peliculas["etiquetas"])
    title = eliminar_numeros_caracteres(pelicula)
    query_vec = vectores.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()

    # Obtener los 5 más similares
    indices_similares = np.argpartition(similarity, -50)[-50:]
    similares = peliculas.iloc[indices_similares]

    # Ordenar los elementos similares por popularidad de mayor a menor
    similares_ordenados = similares.sort_values(by='popularidad', ascending=False)

    # Obtener los 5 elementos más populares
    similares_populares = similares_ordenados.head(5)

    # Retrieve image URLs for recommended movies
    similares_populares["image_url"] = similares_populares["id"].apply(buscar_img)

    return similares_populares[["titulo", "image_url"]].values


lista_peliculas = pickle.load(open("movie_dict.pkl","rb"))
peliculas = pd.DataFrame(lista_peliculas)

similitudes = pickle.load(open("similarity.pkl", "rb"))

original = pickle.load(open("original.pkl","rb"))
original2 = pd.DataFrame(original)

original = pickle.load(open("peliculas1-4.pkl","rb"))
original1 = pd.DataFrame(original)

st.title("**:red[Sistema de recomendacion de peliculas]**")

opcion = st.selectbox(
'Elije una pelicula?',
peliculas["titulo"].values)

if st.button("Recomendaciones"):
    recomendaciones = recomendacion(opcion)
    cols = st.columns(5)
    i = 0  # Inicializar la variable i
    for titulo, image_url in recomendaciones:
        cols[i].image(image_url, use_column_width=True)
        cols[i].write(titulo)
        i += 1

# Funcion #1

# Crear una nueva columna "mes_estreno" con el mes extraído de la columna "release_date"
original1['mes_lanzamiento'] = pd.to_datetime(original1['Fecha_lanzamiento']).dt.month

# Función para obtener la cantidad de filmaciones en un mes específico
def cantidad_filmaciones_mes(mes):
    # Convertir el mes a minúsculas
    mes = str(mes).lower()

    # Mapear los meses en español a los meses en inglés
    meses_map = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }

    # Obtener el número del mes correspondiente
    numero_mes = meses_map.get(mes)

    if numero_mes:
        # Filtrar el DataFrame por el mes de estreno
        df_mes = original1[original1['mes_lanzamiento'] == numero_mes]
        cantidad = len(df_mes)

        return f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"
    else:
        return "Mes no válido"


# Funcion #2

# Crear la columna "dia_semana" a partir de la columna "release_date"
original1['dia_lanzamiento'] = pd.to_datetime(original1['Fecha_lanzamiento']).dt.day_name()

def cantidad_filmaciones_dia(dia):
    # Convertir el día a minúsculas
    dia = dia.lower()

    # Mapear los días en español a los días en inglés
    dias_map = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sábado': 'Saturday',
        'domingo': 'Sunday'
    }

    # Obtener el día correspondiente en inglés
    dia_ingles = dias_map.get(dia)

    if dia_ingles:
        # Filtrar el DataFrame por el día de estreno
        df_dia = original1[original1['dia_lanzamiento'] == dia_ingles]
        cantidad = len(df_dia)

        return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia.capitalize()}"
    else:
        return "Día no válido"


# Funcion #3

# cambiar tipos de datos a la columna popularidad y año_lanzamiento

original1['popularidad'] = original1['popularidad'].astype(float).round(1)
original1['año_lanzamiento'] = original1['año_lanzamiento'].astype(int)
def score_titulo(titulo_de_la_filmación):
    # Filtrar el DataFrame por el título de la filmación
    filtro = original1['titulo'] == titulo_de_la_filmación
    pelicula = original1[filtro]

    if len(pelicula) > 0:
        # Obtener el título, año de estreno y score/popularidad
        titulo = pelicula['titulo'].iloc[0]
        año_estreno = pelicula['año_lanzamiento'].iloc[0]
        score = pelicula['popularidad'].iloc[0]

        return f"La película {titulo} fue estrenada en el año {año_estreno} con un score/popularidad de {score}"
    else:
        return "No se encontró la película"

# Funcion #4

def votos_titulo(titulo_de_lafilmación):
    # Filtrar el DataFrame por el título de la filmación
    filtro = original1['titulo'] == titulo_de_lafilmación
    pelicula = original1[filtro]

    if len(pelicula) > 0:
        # Obtener el título y la cantidad de votos
        titulo = pelicula['titulo'].iloc[0]
        votos = pelicula['conteo_votos'].iloc[0]

        if votos >= 2000:
            # Calcular la suma de votos
            votos_totales = pelicula['conteo_votos'].sum()

            # Calcular el promedio de votos
            promedio_votos = votos_totales / votos

            return f"La película {titulo} cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos:.1f}"
        else:
            return f"La película {titulo} no cumple con la condición de tener al menos 2000 valoraciones"
    else:
        return "No se encontró la película"

# funcion #5

def get_actor(nombre_actor):
    original2['elenco'] = original2['elenco'].astype(str)
    actor_films = original2[original2['elenco'].str.contains(nombre_actor, case=False)]['retorno']
    cantidad_peliculas = actor_films.count()
    if cantidad_peliculas > 0:
        retorno_total = actor_films.sum()
        promedio_retorno = retorno_total / cantidad_peliculas
        return f"El actor {nombre_actor} ha participado en {cantidad_peliculas} películas. Su retorno total es {round(retorno_total, 1)} con un promedio de {round(promedio_retorno, 1)} por película."
    else:
        return f"No se encontraron registros para el actor {nombre_actor}."

# Funcion #6

from tabulate import tabulate

def get_director(nombre_director):
    original2['director'] = original2['director'].astype(str)
    director_films = original2[original2['director'].str.contains(nombre_director, case=False)]
    cantidad_peliculas = director_films.shape[0]

    if cantidad_peliculas > 0:
        retorno_total = director_films['retorno'].sum()
        exito_director = retorno_total / cantidad_peliculas

        peliculas = director_films[['titulo', 'Fecha_lanzamiento', 'retorno', 'presupuesto', 'recaudo']]
        peliculas = peliculas.reset_index(drop=True)

        peliculas_sorted = peliculas.sort_values(by='Fecha_lanzamiento', ascending=False)

        mensaje = f"🎬🎥🌟 ¡Encontré al director {nombre_director}! 🌟🎥🎬\n\n"
        mensaje += f"{nombre_director} ha dirigido {cantidad_peliculas} películas.\n\n"
        mensaje += f"Su éxito se mide a través de un retorno promedio por película de {exito_director:.2f}.⭐\n\n"
        mensaje += "¡Aquí están algunas de las películas dirigidas por este talentoso director:\n\n"
        mensaje += tabulate(peliculas_sorted.values.tolist(), headers=peliculas.columns, tablefmt='pipe') + "\n"

        return mensaje
    else:
        return f"No se encontraron registros para el director {nombre_director}. ¿Quizás ha dirigido películas bajo otro nombre?"


st.title("Panel de consultas")
# Establecer el tema personalizado

# Lista de funciones disponibles
funciones_disponibles = {
    'Cantidad de filmaciones por mes': cantidad_filmaciones_mes,
    'Cantidad de filmaciones por día': cantidad_filmaciones_dia,
    'Rating de una pelicula': score_titulo,
    'Votos de una pelicula': votos_titulo,
    'Información de un actor': get_actor,
    'Información de un director': get_director
}
opcion = st.selectbox('Elige una función:', list(funciones_disponibles.keys()))

# Obtener la función seleccionada
funcion_seleccionada = funciones_disponibles[opcion]

# Ejecutar la consulta 1
if opcion == 'Cantidad de filmaciones por mes':
    # Obtener el texto de entrada del usuario
    nombre_mes = st.text_input('Ingresa el mes:', '')

    # Ejecutar la consulta cuando se presiona el botón
    if st.button('Buscar'):
        resultado = funcion_seleccionada(nombre_mes)
        st.write(resultado)

# Ejecutar la consulta 2
if opcion == 'Cantidad de filmaciones por día':
    # Obtener el texto de entrada del usuario
    nombre_dia = st.text_input('Ingresa el dia:', '')

    # Ejecutar la consulta cuando se presiona el botón
    if st.button('Buscar'):
        resultado = funcion_seleccionada(nombre_dia)
        st.write(resultado)


# Ejecutar la consulta 3
if opcion == 'Rating de una pelicula':
    # Obtener el texto de entrada del usuario
    pelicula1 = st.text_input('Ingresa el nombre de la pelicula:', '')

    # Ejecutar la consulta cuando se presiona el botón
    if st.button('Buscar'):
        resultado = funcion_seleccionada(pelicula1)
        st.write(resultado)

# Ejecutar la consulta 4
if opcion == 'Votos de una pelicula':
    # Obtener el texto de entrada del usuario
    pelicula = st.text_input('Ingresa el nombre de la pelicula:', '')

    # Ejecutar la consulta cuando se presiona el botón
    if st.button('Buscar'):
        resultado = funcion_seleccionada(pelicula)
        st.write(resultado)

# Ejecutar la consulta 5
if opcion == 'Información de un actor':
    # Obtener el texto de entrada del usuario
    actor = st.text_input('Ingresa el nombre del actor:', '')

    # Ejecutar la consulta cuando se presiona el botón
    if st.button('Buscar'):
        resultado = funcion_seleccionada(actor)
        st.write(resultado)

# Ejecutar la consulta 6

if opcion == 'Información de un director':
    # Obtener el texto de entrada del usuario
    director = st.text_input('Ingresa el nombre del director:', '')

    # Ejecutar la consulta cuando se presiona el botón
    if st.button('Buscar'):
        resultado = funcion_seleccionada(director)
        st.write(resultado)


