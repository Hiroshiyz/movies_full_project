from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.db import db_session
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 註冊


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        passowrd = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("使用者已存在")
            return redirect(url_for('auth.register'))
        new_user = User(username=username, email=email)
        new_user.set_password(passowrd)

        db_session.add(new_user)
        db_session.commit()
        # debug用
        # for row in db_session.query(User).all():
        #     print(row.id, row.username, row.created_at,
        #           row.password_hash, row.email)
        print("註冊成功")
        flash("註冊成功請登入")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# 登入
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Base.query繼承可直接User.query.filter_by...
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            print("登入成功")
            return redirect(url_for('movie.hot_movies'))
        flash("帳號密碼錯誤")
    return render_template('login.html')
# 登出


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    print("登出成功")
    flash("登出")
    return redirect(url_for('auth.login'))
