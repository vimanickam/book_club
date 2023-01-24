# Book Club
# Author: Vignesh Manickam

from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def base():
    return render_template("home.html")

@app.route("/signup")
def signup():
    return render_template("register.html")

@app.route("/register",methods=['POST'])
def register():
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "age" : request.form['age'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "confirm_password" : request.form['confirm_password'],
    }
    if User.validate_registration(data):
        data["password"] = bcrypt.generate_password_hash(request.form['password'])
        data["confirm_password"] = bcrypt.generate_password_hash(request.form['confirm_password'])
        result = User.add_user(data)
        session['user_name'] = data['first_name'] + " " + data['last_name']
        session['user_id'] = result
    else :
        return redirect("/signup")
    return redirect("/dashboard")

@app.route("/login",methods=['POST'])
def login():
    data = {
        "email" : request.form['email'],
        "password": request.form['password']
    }
    if User.validate_login(data):
        user_detail = User.get_user_by_email(data['email'])
        if not user_detail:
            flash("invalid email","login")
            return redirect('/')
        if not bcrypt.check_password_hash(user_detail.password,request.form['password']):
            flash("wrong password","login")
            return redirect('/')
        session['user_name'] = user_detail.first_name +" "+ user_detail.last_name
        session['user_id'] = user_detail.id
        return redirect('/dashboard')
    else:
        return redirect('/')

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/favorites")
def favorites():
    print("Inside Favorites Route")
    results = User.get_all_fav_books_id(session.get('user_id'))
    #return redirect('/dashboard')
    return render_template('favorites.html',user=results)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')