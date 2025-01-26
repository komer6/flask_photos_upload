SETUP:

go to backhand directory and copy the following commend to activte the virtual envyyormeant to the terminal
venv\Scripts\activate
(if linux/mac: source venv/bin/activate)

install requirements:
 pip install -r requirements.txt

Start the Application
python app.py
he application will run on http://127.0.0.1:5000/ by default.




Current Functionality
API Endpoints:

User Management
POST /api/add-user: Add a new user (name and email).
GET /api/search-users: Search for users by name or email.
DELETE /api/users/int:user_id: Delete a user by ID.
GET /api/users/int:user_id: Get details of a user by ID.
PUT /api/update-user/int:user_id: Update user information.

Book Management
POST /api/upload-file: Upload a file (image) for a book.
POST /api/upload-metadata: Upload metadata for a book (title, author, year, etc.).
GET /api/books: List all books.
GET /api/search-books: Search for books by title, author, or year.
DELETE /api/books/int:book_id: Delete a book by ID.
GET /uploads/<filename>: Serve uploaded book images.

Loan Management
POST /api/loan-book: Loan a book to a user.
GET /api/user-loans/int:user_id: Get all loans for a specific user.
DELETE /api/delete-loan/int:loan_id: Delete a loan by ID.

Logging
The application logs all important events, such as user and book additions, errors, and requests. Logs are saved in the app.log file.

File Uploads
The uploaded files are stored in the uploads/ directory. Only files with the following extensions are allowed: png, jpg, jpeg, gif.

Technologies Used
Flask: Web framework for building the API.
SQLAlchemy: ORM for interacting with the SQLite database.
SQLite: Lightweight relational database for storing user and book data.
Flask-CORS: Enables CORS for the API.


Prerequisites
Before running the application, make sure you have the following installed on your system:

Python 3.x
pip (Python package manager)