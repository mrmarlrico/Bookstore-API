from pymongo import MongoClient
from fastapi import Depends

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    db = client["bookstore"]
            
    # Create indexes
    db.books.create_index("title")
    db.books.create_index("author")
    db.books.create_index("price")
    db.books.create_index("sales")


    return db
