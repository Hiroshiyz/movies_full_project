from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
# module 可以更安全生成密碼金鑰
from app.db import Base, db_session
from flask_login import UserMixin
# 用class的方式儲存表格
from datetime import datetime


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    # 儲存hash過的密碼
    password_hash = Column(String(128), nullable=False)
    # 紀錄創建時間
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def set_password(self, password):
        """加密儲存"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """檢查密碼"""
        return check_password_hash(self.password_hash, password)


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(200), nullable=False)
    release_date = Column(DateTime, nullable=False)
    director = Column(String(200), nullable=False)
    actor = Column(String(500))

    def __repr__(self):
        return f'<Movie {self.title} load...>'


class Booking(Base):

    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    moive_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    # 對應到其Table內的id值
    booking_time = Column(DateTime, nullable=False)
    # 讓python直接用oop的方式查詢
    user = relationship("User", back_populates="bookings")
    movie = relationship("Movie", back_populates="bookings")


User.bookings = relationship("Booking", back_populates="user")
Movie.bookings = relationship("Booking", back_populates="movie")
