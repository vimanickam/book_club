# Book Club
# Author: Vignesh Manickam

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import book
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
DB = "books"
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.book_list = []
    
    @classmethod
    def get_user_by_email(cls,user_email):
        data = {"email":user_email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if len(results) < 1 :
            return False
        return cls(results[0])
    
    @classmethod
    def get_all_users_books(cls):
        #print("Get all User details with books")
        query = "SELECT * FROM books LEFT JOIN users ON books.user_id = users.id;"
        results = connectToMySQL(DB).query_db(query)
        #print("results = ",results)
        return results

    @classmethod
    def get_all_users_books_id(cls,id):
        #print("Get all User details with books with ID")
        data = {
            "id":id
        }
        #print("Get all User details with books")
        query = "SELECT * FROM users LEFT JOIN books ON books.user_id = users.id WHERE books.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        #print("results = ",results)
        return results

    @classmethod
    def get_all_fav_books_id(cls,id):
        #print("Inside Get all Favorite Books")
        data = {
            "id": id
        }
        query = """
            SELECT * FROM users
            LEFT JOIN favorites ON users.id = favorites.user_id
            LEFT JOIN books ON books.id = favorites.book_id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DB).query_db(query,data)
        #print(results)
        user = cls(results[0])
        for row in results:
            fav_books_info = {
                "id":row['books.id'],
                "name": row['name'],
                "author": row['author'],
                "description": row['description'],
                "user_id": row['books.user_id'],
                "created_at": row['books.created_at'],
                "updated_at": row['books.updated_at']
            }
            user.book_list.append(book.Book(fav_books_info))
        return user

    @classmethod
    def add_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,age,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(age)s,%(email)s,%(password)s,NOW(),NOW());"
        results = connectToMySQL(DB).query_db(query,data)
        return results
    
    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name should have atleast 2 Characters","register")
            is_valid = False
        if len(user['last_name']) < 2 :
            flash("Last Name should have atleast 2 Characters","register")
            is_valid = False
        if len(user['age']) < 2 :
            flash("Age cannot be empty","register")
            is_valid = False
        if len(user['email']) == 0 :
            flash("Email cannot be empty","register")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address","register")
            is_valid = False
        if len(user['password']) < 8 :
            flash("Password should have atleast 8 Characters","register")
            is_valid = False
        elif not PASSWORD_REGEX.match(user['password']):
            flash("Password should contain atleast 1 Upper case and 1 Number","register")
            is_valid = False
        if len(user['confirm_password']) < 8 :
            flash("Confirm Password should have atleast 8 Characters","register")
            is_valid = False
        if not (user['password'] == user['confirm_password']) :
            flash("Password and Confirm Password is NOT matching","register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) == 0 :
            flash("Email cannot be empty","login")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address","login")
            is_valid = False
        if len(user['password']) == 0 :
            flash("Password cannot be empty","login")
            is_valid = False
        return is_valid