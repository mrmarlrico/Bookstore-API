# CPSC 449 - Final Project

## Members

- Marl Rico - mrmarlrico@csu.fullerton.edu

## Project Description

<!-- Add stuff here -->

## Project Requirements

1. Install MongoDB
   - Visit the MongoDB Download Center at https://www.mongodb.com/try/download/community.
   - Choose the "Windows" tab, select the desired version, and download the MSI installer.
   - Run the installer and follow the installation wizard.
   - Add the MongoDB bin folder (usually located at C:\Program Files\MongoDB\Server\[version]\bin) to your system's PATH environment variable.
2. Install virtual environment "python3 -m pip install --user virtualenv"
3. Run virtual environment "python3 -m venv env"
4. Activate virtual environment "source env/bin/activate"
5. Install requirements "pip install -r requirements.txt"

## How To Use

1. Run MongoDB
2. Run the app "python run.py"
3. Adding new book to the store

   - On Linux/Ubuntu terminal use this code
   - "curl -X POST -H "Content-Type: application/json" -d '{
     "title": "The Great Gatsby",
     "author": "F. Scott Fitzgerald",
     "description": "A novel set in the Roaring Twenties, about the mysterious Jay Gatsby.",
     "price": 12.99,
     "stock": 75
     }' http://localhost:8000/books"

4. Retrieving a list of all books in the store

   - On your web browser type "http://localhost:8000/books"

5. Retrieving a specific book by ID

   - On Linux/Ubuntu terminal use this code
   - On your web browser type "http://localhost:8000/books/{bookid}
   - Replace {bookid} with bookid that needs to be retrieved

6. Updating an existing book by ID

   - On Linux/Ubuntu terminal use this code
   - curl -X PUT -H "Content-Type: application/json" -d '{
     "title": "Updated Book Title",
     "author": "Updated Author Name",
     "description": "This is the updated book description",
     "price": 15.99,
     "stock": 200
     }' http://localhost:8000/books/{book_id}
   - Replace {bookid} with bookid that needs to be updated

7. Deleting a book from the store by ID

   - On Linux/Ubuntu terminal use this code
   - curl -X DELETE http://localhost:8000/books/{book_id}
   - Replace {bookid} with bookid that needs to be deleted

8. Searching for books by title, author, and price range

   - On Linux/Ubuntu terminal use this code
   - curl "http://localhost:8000/search?title=Title&author=Author&min_price=10&max_price=50"
