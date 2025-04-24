from flask import Blueprint, render_template, current_app

import requests
movie_bp = Blueprint('movie', __name__, url_prefix='/movies')
# 'movie'這是 Blueprint 的名稱，在後續 debug、url_for() 時會用到（如 url_for('movie.movie_home')）
# __name__	告訴 Flask 目前這個 Blueprint 是在哪個模組（會影響路徑解析、錯誤提示）
# url_prefix	所有這個 Blueprint 裡的路由都會加上這個前綴。例如這裡加了 /movies，所以你才會在 /movies/ 底下看到這些 route

# hot


@movie_bp.route('/')
def hot_movies():
    API_KEY = current_app.config['TMDB_API_KEY']
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=zh-TW&page=1"
    response = requests.get(url)
    movies = response.json().get('results', [])
    return render_template('index.html', movies=movies)

# 即將上映


@movie_bp.route('/all')
def all_movies():
    API_KEY = current_app.config['TMDB_API_KEY']
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=zh-TW&page=1"

    response = requests.get(url)
    movies = response.json().get('results', [])
    return render_template('all.html', movies=movies)


# search


# @movie_bp.route('/search')
# def search_movies():
#     keyword = request.value('')
#     return render_template('search_results.html', keyword=keyword)


# single movie

@movie_bp.route('/<int:movie_id>')
def movie_detail(movie_id):
    API_KEY = current_app.config['TMDB_API_KEY']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=zh-TW&page=1"
    response = requests.get(url)
    if response.status_code != 200:
        return "Movie not found", 404
    movie = response.json()
    # print(movie)
    return render_template('detail.html', movie_id=movie_id, movie=movie)
