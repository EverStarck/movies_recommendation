import os
import requests
import pickle


movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

def get_movies_list():
    list = []

    for movie in range(0,len(movies)):
        list.append({
            "label": movies.iloc[movie].title,
            "value": str(movies.iloc[movie].movie_id)
        })

    return list


def tmdb_info(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('TMDB_API')}&language=en-US"
    data = requests.get(url)

    if data.status_code != 200:
        return {
            "error": True,
            "message": "Movie not found.",
            "data": {
                "full_path": "https://www.movienewz.com/img/films/poster-holder.jpg",
                "backdrop_path": "https://www.movienewz.com/img/films/backdrop-holder.jpg"
            }
        }

    data = data.json()

    return {
        "error": False,
        "message": "Movie found.",
        "data": {
            "full_path": f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
             **data
        }
    }


def recommend(movie):
    movie = movies[movies['title'] == movie]

    if len(movie) == 0:
        return None

    index = movie.index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = {}

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies[int(movie_id)] = ({
            "movie_id": int(movie_id),
            "title": movies.iloc[i[0]].title,
            "vote_average": int(movies.iloc[i[0]].vote_average),
            "vote_count": int(movies.iloc[i[0]].vote_count),
            "tags": movies.iloc[i[0]].tags,
            "tmdb":tmdb_info(movie_id)
        })

    recommended_movies[int(movie.iloc[0].movie_id)] = {
        "movie_id": int(movie.iloc[0].movie_id),
        "title": movie.iloc[0].title,
        "vote_average": int(movie.iloc[0].vote_average),
        "vote_count": int(movie.iloc[0].vote_count),
        "tags": movie.iloc[0].tags,
        "tmdb": tmdb_info(movie.iloc[0].movie_id),
    }

    return recommended_movies