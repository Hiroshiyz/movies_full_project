from app.db import db_session
from app.models import Movie, Seat
import requests
from app.models import Movie
from app.db import db_session
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv('TMDB_API_KEY')


def seed_movies():

    url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=zh-TW&page=1"
    response = requests.get(url)
    data = response.json()

    for item in data['results']:
        exists = db_session.query(Movie).filter_by(id=item['id']).first()
        if exists:
            continue
        movie = Movie(
            id=item['id'],
            title=item['title'],
            description=item['overview'],
            release_date=item['release_date']
        )
        db_session.add(movie)
        print(f"已新增電影：{movie.title}")
        db_session.commit()
    print("所有熱門電影已儲存")


def create_seat():
    seat_rows = ['a', 'b', 'c', 'd']
    movies = db_session.query(Movie).all()
    for movie in movies:
        # 檢查是否有座位
        existing_seats = db_session.query(
            Seat).filter_by(movie_id=movie.id).count()
        if existing_seats > 0:
            print(f'電影{movie.title}已經有座位')
            continue

        for row in seat_rows:
            for num in range(1, 5):
                seat_number = f'{row}{num}'
                seat = Seat(seat_number=seat_number, movie_id=movie.id)
                db_session.add(seat)
        print(f'已經新增4x4座位給{movie.title}')
    db_session.commit()
    print("所有電影初始化")


if __name__ == "__main__":
    seed_movies()
    create_seat()
