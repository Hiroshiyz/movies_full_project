from flask import Blueprint, render_template, request, redirect, current_app, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import requests
from app.models import User, Movie, Booking
from app.db import db_session
order_bp = Blueprint('booking', __name__, url_prefix='/booking')

# 訂購頁面


@order_bp.route('/<int:movie_id>', methods=['POST', 'GET'])
@login_required
def book_ticket(movie_id):
    # API抓取資料渲染
    API_KEY = current_app.config['TMDB_API_KEY']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=zh-TW&page=1"
    response = requests.get(url)
    movie = response.json()
    if request.method == "POST":
        new_movie = db_session.query(Movie).filter_by(id=movie_id).first()
        if not new_movie:
            # 將電影資料抓下
            movie_data = Movie(id=movie['id'],
                               title=movie['title'],
                               description=movie['overview'],
                               release_date=movie['release_date'],
                               )
            db_session.add(movie_data)
        # 建立訂單
        user_id = current_user.id
        # 將html的date轉成 datetime object
        date_str = request.values['booking_time']
        booking_time = datetime.strptime(date_str, "%Y-%m-%d")
        new_booking = Booking(
            user_id=user_id,
            movie_id=movie_id,
            booking_time=booking_time
        )
        db_session.add(new_booking)
        db_session.commit()
        return redirect(url_for('booking.history'))
    # 限制下單時間
    today = datetime.today().date()
    last_day = today + timedelta(days=14)
    flash("下單成功")
    return render_template('order.html', movie=movie, movie_id=movie_id, today=today, last_day=last_day)

# 歷史訂單


@order_bp.route('/history')
def history():
    bookings = db_session.query(Booking).all()
    return render_template('history.html', bookings=bookings)
