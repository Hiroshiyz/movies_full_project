from flask import Blueprint, render_template, request, redirect, current_app, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import requests
from app.models import User, Movie, Booking, Seat
from app.db import db_session
order_bp = Blueprint('booking', __name__, url_prefix='/booking')

# 訂購頁面


@order_bp.route('/<int:movie_id>', methods=['POST', 'GET'])
@login_required
def book_ticket(movie_id):
    # 從資料庫抓資料
    movie = db_session.query(Movie).filter_by(id=movie_id).first()
    if not movie:
        flash("找不到此電影")
        return redirect(url_for('movie.hot_movies'))

    # 這部分是處理 POST 請求，建立訂單
    if request.method == "POST":
        # 取得座位 ID
        seat_id = request.values.get('seat_id')
        seat = db_session.query(Seat).filter_by(
            id=seat_id, movie_id=movie_id).first()

        if not seat:
            flash("座位不存在")
            return redirect(url_for('booking.book_ticket', movie_id=movie_id))

        # 檢查座位是否已被預定
        if seat.is_taken:
            flash("座位已被預定")
            return redirect(url_for('booking.book_ticket', movie_id=movie_id))

        # 設定座位為已被預定
        seat.is_taken = True

        # 取得使用者的 ID
        user_id = current_user.id

        # 解析傳來的 booking_time 並轉換為 datetime 物件
        date_str = request.values['booking_time']
        booking_time = datetime.strptime(
            date_str, "%Y-%m-%dT%H:%M")  # 這裡將字串轉換為 datetime 物件

        # 建立新訂單並保存到資料庫
        new_booking = Booking(
            user_id=user_id,
            seat_id=seat.id,
            movie_id=movie_id,
            booking_time=booking_time
        )

        db_session.add(new_booking)
        db_session.commit()

        flash("下單成功")
        return redirect(url_for('booking.history'))

    # 限制下單時間範圍，可以設置例如今天和兩週後的日期
    today = datetime.today().date()
    last_day = today + timedelta(days=14)

    # 查詢該電影所有座位
    seats = db_session.query(Seat).filter_by(movie_id=movie_id).all()

    # 查詢該時間點所有已被預定的座位
    # 這裡根據選擇的時間來查詢
    booked_seats = db_session.query(Booking).filter(
        Booking.movie_id == movie_id).all()
    booked_seat_ids = [booking.seat_id for booking in booked_seats]

    # 傳遞座位、已預定的座位 ID 和選擇的時間到前端
    return render_template('order.html', movie=movie, movie_id=movie_id, seats=seats, booked_seat_ids=booked_seat_ids, today=today, last_day=last_day)
# 歷史訂單


@order_bp.route('/history')
def history():
    user_id = current_user.id
    bookings = db_session.query(Booking).filter_by(user_id=user_id).all()

    return render_template('history.html', bookings=bookings)


@order_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    db_session.query(Booking).filter_by(id=id).delete()
    db_session.commit()
    return redirect(url_for('booking.history'))
