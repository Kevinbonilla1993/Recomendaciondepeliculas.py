# Proyecto: Sistema de Recomendación y Tablero de Consultas

## Descripción

El proyecto **Sistema de Recomendación y Tablero de Consultas** es una aplicación que ofrece una interfaz fácil de manejar, diseñada para brindar recomendaciones de películas personalizadas y proporcionar consultas relacionadas con información cinematográfica. Utiliza técnicas de recomendación basadas en similitudes entre películas, empleando la biblioteca Tensorflow para realizar dichos cálculos. Además, el desarrollo de la interfaz se realizó utilizando Streamlit, una herramienta que facilita la creación de aplicaciones web interactivas.

### Funcionalidades principales

La aplicación consta de dos componentes principales:

1. **Recomendaciones de películas**: La interfaz permite al usuario elegir una película y, en base a ella, obtener hasta 5 recomendaciones de películas similares. Estas recomendaciones se generan utilizando el modelo de recomendación basado en Tensorflow, que encuentra películas con características y géneros similares.

2. **Tablero de consultas**: El tablero de consultas ofrece una variedad de consultas predefinidas para obtener información sobre películas y personalidades relacionadas. Las consultas disponibles incluyen:

   - Cantidad de filmaciones por mes.
   - Cantidad de filmaciones por día.
   - Rating de una película.
   - Votos de una película.
   - Información de un actor.
   - Información de un director.

### Procesamiento de datos

Antes de desarrollar este proyecto, se realizó una limpieza de datos y transformaciones ETL (Extract, Transform, Load). Esto involucró varias tareas, como el renombramiento de columnas, la desanidación de columnas, el cambio de tipos de datos, la ordenación de fechas y la eliminación de columnas y filas irrelevantes. Los datos utilizados en el proyecto provienen de dos archivos CSV llamados "movies" y "credits", que se fusionaron utilizando la operación de merge para trabajar con ellos de manera conjunta. Además, se extrajeron datos adicionales de la API de la base de datos de películas para obtener enlaces de imágenes y poder mostrarlos adecuadamente en la interfaz.


### Uso

Puedes acceder a la aplicación en línea a través de este [App](https://kevinbonilla1993-recomendaciondepeliculas-py-app-8nlu23.streamlit.app/). La aplicación está alojada en Streamlit Share, lo que permite utilizarla sin necesidad de realizar ninguna instalación local.

Además, puedes ver un video demostrativo del funcionamiento de la aplicación [Video]((https://vimeo.com/835727155?share=copy).

Si deseas utilizar la API, puedes acceder a ella a través de [API](https://api-consultas-czfj.onrender.com/docs#/), y el repositotio de la api [Repositorio API](https://github.com/Kevinbonilla1993/fastapi)

## Código fuente

El código fuente del proyecto está disponible en [Google Drive](https://drive.google.com/drive/folders/1LuxN3N9PxZWIux8arnEBtEC0xDeBCmpi?usp=drive_link), donde puedes acceder y revisar el código utilizado en la aplicación.




