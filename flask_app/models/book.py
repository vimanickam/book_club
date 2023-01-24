# Book Club
# Author: Vignesh Manickam

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

DB="books"

class Book:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.author = data['author']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.fav_users_lists=[]
    
    @classmethod
    def add_book(cls,data):
        query = "INSERT INTO books (name,author,description,user_id,created_at,updated_at) VALUES (%(name)s,%(author)s,%(description)s,%(user_id)s,NOW(),NOW());"
        results = connectToMySQL(DB).query_db(query,data)
        #print("------Book Insertion-----")
        #print("Results = ",results)
        return results

    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books"
        results = connectToMySQL(DB).query_db(query)
        #print("Get all Books Results")
        #print(results)
        all_books = []
        for each_book in results :
            all_books.append(cls(each_book))
        return all_books

    @classmethod
    def get_book_id(cls,id):
        data = {
            "id":id
        }
        query = "SELECT * from books WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        #print("----Get Book By ID-----")
        #print("result = ", result)
        return (cls(result[0]))

    @classmethod
    def update_book(cls,data):
        #print("Inside the Update Method")
        query = "UPDATE books SET name=%(name)s, author=%(author)s, description=%(description)s WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        #print ("Update Result = ", result)
        return result

    @classmethod
    def delete_book_id(cls,id):
        #print("inside Delete method")
        data = {
            "id":id
        }
        query = "DELETE from books WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        #print("Delete result = ", result)
        return (result)

    @classmethod
    def add_fav_book(cls,data):
        #print("inside Favorite Insertion")
        query = "INSERT INTO favorites (user_id,book_id,created_at,updated_at) VALUES (%(user_id)s,%(book_id)s,NOW(),NOW());"
        result = connectToMySQL(DB).query_db(query,data)
        #print("Result of Fav = ", result)
        return result

    @classmethod
    def delete_fav_book(cls,data):
        #print("inside Delete Fav book")
        query = "DELETE from favorites WHERE user_id = %(user_id)s AND book_id = %(book_id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        #print("Delete result = ", result)
        return (result)
        
    @classmethod
    def check_fav_book(cls,data):
        #print("inside check favorite")
        query = "SELECT * FROM favorites Where user_id = %(user_id)s AND book_id = %(book_id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        if (len(result) == 0):
            return False
        return (True)

    @classmethod
    def get_all_fav_users_book(cls,id):
        #print("inside Getting all users who liked this book")
        data = {
            "id":id
        }
        query = """
            SELECT * from books 
            LEFT JOIN users AS creator ON creator.id = books.user_id
            LEFT JOIN favorites ON books.id = favorites.book_id
            LEFT JOIN users AS fav_user ON fav_user.id = favorites.user_id
            where books.id=%(id)s;
        """
        results = connectToMySQL(DB).query_db(query,data)
        book = cls(results[0])
        for row in results:
            user_fav_info = {
                "id": row['fav_user.id'],
                "first_name": row['fav_user.first_name'],
                "last_name": row['fav_user.last_name'],
                "age": row['fav_user.age'],
                "email": row['fav_user.email'],
                "password": row['fav_user.password'],
                "created_at": row['fav_user.created_at'],
                "updated_at": row['fav_user.updated_at']
            }
            book.fav_users_lists.append(user.User(user_fav_info))
        
        #print("REsult = ", results)
        return book

    @staticmethod
    def validate_book(book):
        #print("Inside Book Validation")
        is_valid = True
        if len(book['name']) < 2:
            flash("Book Name should have atleast 2 Characters","book")
            is_valid = False
        if len(book['author']) < 2 :
            flash("Author should have atleast 2 Characters","book")
            is_valid = False
        if len(book['description']) < 2 :
            flash("Description cannot be empty","book")
            is_valid = False
        return is_valid