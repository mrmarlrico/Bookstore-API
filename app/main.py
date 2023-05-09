from fastapi import APIRouter, Depends, HTTPException
from .models import Book
from .database import get_db
from fastapi import FastAPI
from bson import ObjectId

app = FastAPI()

# GET /books: Retrieves a list of all books in the store
@app.get("/books")
def get_all_books(db=Depends(get_db)):
    books = list(db.books.find())
    for book in books:
        book["_id"] = str(book["_id"])
    return books

# GET /books/{book_id}: Retrieves a specific book by ID
@app.get("/books/{book_id}")
def get_book_by_id(book_id: str, db=Depends(get_db)):
    book = db.books.find_one({"_id": ObjectId(book_id)})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book["_id"] = str(book["_id"])
    return book

# POST /books: Adds a new book to the store
@app.post("/books")
def create_book(book: Book, db=Depends(get_db)):
    book_data = book.dict()

    # Validate the book data
    if book_data["price"] < 0 or book_data["stock"] < 0:
        raise HTTPException(status_code=400, detail="Invalid price or stock")

    # Store the book in MongoDB
    result = db.books.insert_one(book_data)
    book_data["_id"] = str(result.inserted_id)

    return book_data

# PUT /books/{book_id}: Updates an existing book by ID
@app.put("/books/{book_id}")
def update_book(book_id: str, book: Book, db=Depends(get_db)):
    book_data = book.dict()
    result = db.books.update_one({"_id": ObjectId(book_id)}, {"$set": book_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"updated_book": book_data}

# DELETE /books/{book_id}: Deletes a book from the store by ID
@app.delete("/books/{book_id}")
def delete_book(book_id: str, db=Depends(get_db)):
    result = db.books.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"deleted_book_id": book_id}

# GET /search?title={}&author={}&min_price={}&max_price={}: Searches for books by title, author, and price range
@app.get("/search")
def search_books(title: str = None, author: str = None, min_price: float = None, max_price: float = None, db=Depends(get_db)):
    query = {}
    if title:
        query["title"] = title
    if author:
        query["author"] = author
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price

    search_result = list(db.books.find(query))
    for book in search_result:
        book["_id"] = str(book["_id"])
    return search_result

@app.get("/total_books")
def get_total_books(db=Depends(get_db)):
    total_books = db.books.count_documents({})
    return {"total_books": total_books}

@app.get("/top_5_bestselling_books")
def get_top_5_bestselling_books(db=Depends(get_db)):
    pipeline = [
        {"$sort": {"sales": -1}},
        {"$limit": 5},
        {"$project": {"_id": 0, "title": 1, "author": 1, "sales": 1}}
    ]
    top_5_books = list(db.books.aggregate(pipeline))
    return top_5_books

@app.get("/top_5_authors")
def get_top_5_authors(db=Depends(get_db)):
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
        {"$project": {"_id": 0, "author": "$_id", "book_count": "$count"}}
    ]
    top_5_authors = list(db.books.aggregate(pipeline))
    return top_5_authors
