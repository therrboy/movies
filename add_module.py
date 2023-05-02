import requests

data_for_use = "https://api.themoviedb.org/3/search/movie?"
key = "af8c88a89a8a18bacfdf356112c09632"
ruta_base_img = "https://image.tmdb.org/t/p/w500"
ruta_id = "https://api.themoviedb.org/3/movie/"

def buscador(query):  # Buscador de la API que nos da toda la info de la pelicula que necesitamos
    parametros = {
        "api_key": key,
        "query": query,
    }
    response = requests.get(data_for_use, params=parametros)
    response.raise_for_status()
    movie_data = response.json()

    movies_list = []
    for movie in range(len(movie_data["results"])):
        poster_path = movie_data["results"][movie]["poster_path"]
        full_poster_path = None
        if poster_path is not None:
            full_poster_path = ruta_base_img + poster_path
        movie_dict = {
            "title": movie_data["results"][movie]["original_title"],
            "release_data": movie_data["results"][movie]["release_date"],
            "poster": full_poster_path,
            "description": movie_data["results"][movie]["overview"],
            "id": movie_data["results"][movie]["id"]
        }
        movies_list.append(movie_dict)
    return movies_list

def pelicula(id):  # Buscador con ID de pelicula, que nos da informacion especifica de la pagina, cuando ya elejimos
    ruta_id = f"https://api.themoviedb.org/3/movie/{id}"
    parametros = {
        "api_key": key
    }
    response = requests.get(ruta_id, params=parametros)
    response.raise_for_status()
    new_movie_data = response.json()
    return new_movie_data

