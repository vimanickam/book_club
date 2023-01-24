# Book Club
# Author: Vignesh Manickam

from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.book import Book
from flask_app.models.user import User

@app.route("/dashboard")
def home():
    if (session.get('user_id') != None ):
        print("Inside Dashboard Route")
        all_books = Book.get_all_books()
        #print("Book Details = ",all_books)
        result = User.get_all_users_books()
        #print(result)
        return render_template("dashboard.html",book_lists = result)
    else :
        return redirect('/')

@app.route("/add-book",methods=['POST'])
def add_book():
    data = {
        "name": request.form['name'],
        "author" : request.form['author'],
        "description": request.form['description'],
        "user_id": session.get('user_id')
    }
    if Book.validate_book(data):
        result = Book.add_book(data)
        #print("After Book Insertion = ",result)
    else :
        return redirect('/add')
    return redirect('/dashboard')

@app.route("/show/<int:id>")
def show_book(id):
    print("Inside Show Route")
    #print("ID = ",id)
    book_data = Book.get_book_id(id)
    data = {
        "user_id":session.get('user_id'),
        "book_id": id
    }
    result = Book.check_fav_book(data)
    if (result) :
        fav = False
    else :
        fav = True
    #print("Book Data = ",book_data)
    #print("Fav Data = ",fav)
    #print("Fav Result = ",result)
    book_data = Book.get_all_fav_users_book(id)
    return render_template("show.html",book=book_data,fav_value = fav)

@app.route("/edit/<int:id>")
def edit_book(id):
    print("Inside Edit Route")
    #print("ID = ",id)
    book_data = Book.get_book_id(id)
    #print("Book Data = ",book_data)
    return render_template("edit.html",book=book_data)

@app.route("/update-book",methods=['POST'])
def update():
    print("inside Update book route")
    data = {
        "id": request.form['id'],
        "name":request.form['name'],
        "author": request.form['author'],
        "description": request.form['description']
    }
    if Book.validate_book(data):
        result = Book.update_book(data)
        print("Update Route result")
    else :
        return redirect(f"/edit/{request.form['id']}")
    return redirect('/dashboard')

@app.route("/delete/<int:id>")
def delete_book(id):
    print("Inside Delete Route")
    #print("ID = ",id)
    book_data = Book.delete_book_id(id)
    #print("Book Data = ",book_data)
    return redirect('/dashboard')

@app.route("/add-fav/<int:book_id>")
def add_fav(book_id):
    print("Inside the Favorite Addition Route")
    data = {
        "user_id":session.get('user_id'),
        "book_id":book_id
    }
    result = Book.add_fav_book(data)
    return redirect(f"/show/{book_id}")
    #return redirect('/dashboard')

@app.route("/remove-fav/<int:book_id>")
def del_fav(book_id):
    print("Inside the Remove Favorite")
    data = {
        "user_id":session.get('user_id'),
        "book_id":book_id
    }
    result = Book.delete_fav_book(data)
    #print("Result = ",result)
    return redirect(f"/show/{book_id}")