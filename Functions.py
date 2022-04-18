import requests


def get_list(movie_name):
    moviesdb_key = "a954f83dfc23eaa6a683daa276f6e570"
    moviesdb_url = "https://api.themoviedb.org/3/search/movie"

    parameters = {
        "api_key": moviesdb_key,
        "query": movie_name
    }

    response = requests.get(moviesdb_url, params=parameters)
    response = response.json()
    response = response["results"]
    list_of_movies = []
    for movie in response:
        movie_dict = {"id": movie["id"], "title": movie["title"], "release_date": movie["release_date"]}
        list_of_movies.append(movie_dict)
    return list_of_movies


def get_movie_details(movie_id):
    moviesdb_key = "a954f83dfc23eaa6a683daa276f6e570"
    moviesdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    parameters = {
        "api_key": moviesdb_key,
        }

    response = requests.get(moviesdb_url, params=parameters)
    response = response.json()
    movie_details_dict = {}
    movie_details_dict["title"] = response['title']
    movie_details_dict["img_url"] = "https://image.tmdb.org/t/p/original/"+response['poster_path']
    movie_details_dict["year"] = response['release_date']
    movie_details_dict["description"] = response['overview']
    movie_details_dict["ranking"]=0
    return movie_details_dict
#
# print(get_list("Batman"))
# print(get_movie_details(414906))