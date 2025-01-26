import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import logging      

# Configure the logger
logging.basicConfig(
    filename="app.log",  # Log file
    level=logging.INFO,  # Logging level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)



app = Flask(__name__)
CORS(app)  # Enable CORS

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max size 16 MB

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    original_name = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    loandate = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "original_name": self.original_name,
            "name": self.name,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "amount": self.amount,
            "loandate": self.loandate,
            "image": self.image,
        }

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    
    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
            "return_date": self.return_date.strftime('%Y-%m-%d %H:%M:%S') if self.return_date else None,
        }






# user page where you can make and return loans

@app.route('/api/add-user', methods=['POST'])
def add_user():
    app.logger.info("Received a request to add a user.")
    data = request.get_json()
    
    # Extracting the data from the request
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        app.logger.info("no name or an emil in user")
        return jsonify({'error': 'Name and email are required'}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        app.logger.info("user alredy created before")
        return jsonify({'error': 'Email already registered'}), 400

    # Create a new user
    new_user = User(name=name, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
        app.logger.info("added user to db")
        return jsonify({'message': 'User added successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



# API: Upload file
@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    app.logger.info("uploadind a book img")
    if 'file' not in request.files:
        app.logger.info("no file u[loaded]")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        original_name = file.filename
        unique_filename = f"{uuid.uuid4().hex}_{original_name}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        app.logger.info("added file")
        return jsonify({'message': 'File uploaded successfully', 'filename': unique_filename}), 200

    app.logger.info("file failure")
    return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif.'}), 400

# API: Upload metadata
@app.route('/api/upload-metadata', methods=['POST'])
def upload_metadata():
    app.logger.info("accesed route to add book to db")
    data = request.get_json()

    # Validate required fields
    required_fields = ['filename', 'name', 'author', 'genre', 'year', 'amount', 'loandate']
    for field in required_fields:
        if field not in data:
            app.logger.info("missing stuff in book and shit")
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        # Save metadata to the database
        book = Book(
            filename=data['filename'],
            original_name=data['filename'],
            name=data['name'],
            author=data['author'],
            genre=data['genre'],
            year=int(data['year']),
            amount=int(data['amount']),
            loandate=int(data['loandate']),
            image=data['filename']
        )
        db.session.add(book)
        db.session.commit()
        app.logger.info("added book")
        return jsonify({'message': 'Metadata uploaded successfully', 'book': book.to_dict()}), 200
    except ValueError:
        app.logger.info("failed to add")
        return jsonify({'error': 'Invalid value for numeric fields'}), 400

# API: List books
@app.route('/api/books', methods=['GET'])
def list_books():
    app.logger.info("ge all book func, i think i delted the stuff i used it fore logger for test i guess?")
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

# API: Search books by title, author, and/or year
@app.route('/api/search-books', methods=['GET'])
def search_books():
    app.logger.info("Accessed search-books endpoint")
    
    # Get query parameters
    title = request.args.get('title')
    author = request.args.get('author')
    year = request.args.get('year')

    query = Book.query

    # Log conditions and filters applied
    if title:
        app.logger.info(f"Searching by title: {title}")
        query = query.filter(Book.name.ilike(f'%{title}%'))
    if author:
        app.logger.info(f"Searching by author: {author}")
        query = query.filter(Book.author.ilike(f'%{author}%'))
    if year:
        app.logger.info(f"Searching by year: {year}")
        query = query.filter(Book.year == int(year))

    try:
        books = query.all()
        if books:
            app.logger.info(f"Found {len(books)} books matching the search criteria.")
        else:
            app.logger.info("No books found matching the search criteria.")
        
        return jsonify([book.to_dict() for book in books]), 200
    
    except Exception as e:
        app.logger.error(f"Error occurred during search: {str(e)}")
        return jsonify({"error": "An error occurred while searching for books."}), 500

# API: Search users by name or email
@app.route('/api/search-users', methods=['GET'])
def search_users():
    app.logger.info("serach user route acessed")
    search_term = request.args.get('name') or request.args.get('email')
    search_by = 'name' if 'name' in request.args else 'email'

    if not search_term:
        app.logger.info("missaing search shoudlnt happem on live beacuse of html i think")
        return jsonify({'error': 'Missing search term'}), 400


    if search_by == 'name':
        app.logger.info("search by name")
        users = User.query.filter(User.name.ilike(f'%{search_term}%')).all()
    else:
        app.logger.info("search by user")
        users = User.query.filter(User.email.ilike(f'%{search_term}%')).all()

    return jsonify([user.to_dict() for user in users]), 200

# Serve uploaded files images and stuff
@app.route('/uploads/<filename>', methods=['GET'])
def get_file(filename):
    app.logger.info("upload a file")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API: Delete a user by ID
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    app.logger.info(f'Received request to delete user with ID: {user_id}')
    
    user = User.query.get(user_id)
    
    if user:
        # Delete all loans associated with this user
        loans = Loan.query.filter_by(user_id=user_id).all()
        
        # Delete each loan
        for loan in loans:
            db.session.delete(loan)
        
        # Commit the changes to remove the loans
        db.session.commit()

        # Now, delete the user
        db.session.delete(user)
        db.session.commit()
        
        app.logger.info(f'User {user_id} and all associated loans deleted successfully')
        return jsonify({'message': 'User and all associated loans deleted successfully'}), 200
    else:
        app.logger.warning(f'User {user_id} not found')
        return jsonify({'error': 'User not found'}), 404


# API: Delete a book by ID
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    app.logger.info(f'Received request to delete book with ID: {book_id}')
    
    book = Book.query.get(book_id)
    
    if book:
        # Delete all loans associated with this book
        loans = Loan.query.filter_by(book_id=book_id).all()
        
        # Delete each loan
        for loan in loans:
            db.session.delete(loan)
        
        # Commit the changes to remove the loans
        db.session.commit()

        # Now, delete the book
        db.session.delete(book)
        db.session.commit()
        
        app.logger.info(f'Book {book_id} and all associated loans deleted successfully')
        return jsonify({'message': 'Book and all associated loans deleted successfully'}), 200
    else:
        app.logger.warning(f'Book {book_id} not found')
        return jsonify({'error': 'Book not found'}), 404

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    app.logger.info(f'Received request to get user with ID: {user_id}')
    
    user = User.query.get(user_id)
    
    if user:
        app.logger.info(f'User {user_id} found: {user.to_dict()}')
        return jsonify(user.to_dict()), 200
    else:
        app.logger.warning(f'User {user_id} not found')
        return jsonify({'error': 'User not found'}), 404

# Home route, did it as a test and forgat about it

@app.route('/')
def home():
    # Log the request to the home endpoint
    app.logger.info("Accessed the home route.")
    return "Welcome to the Book API! Use the API to interact with books and users."




#add a book route
@app.route('/api/loan-book', methods=['POST'])
def loan_book():
    data = request.get_json()
    user_id = data.get('userId')
    book_id = data.get('bookId')

    app.logger.info(f'Received loan request for user_id: {user_id} and book_id: {book_id}')

    if not user_id or not book_id:
        app.logger.warning('Missing user or book ID')
        return jsonify({'error': 'Missing user or book ID'}), 400

    # Check if the user has already loaned this book 
    existing_loan = Loan.query.filter_by(user_id=user_id, book_id=book_id).first()
    if existing_loan:
        app.logger.warning(f'User {user_id} has already loaned book {book_id}')
        return jsonify({'error': 'You have already loaned this book.'}), 400

    # Check if the user has any overdue loans
    overdue_loan = Loan.query.filter_by(user_id=user_id).filter(Loan.return_date < datetime.utcnow()).first()
    if overdue_loan:
        app.logger.warning(f'User {user_id} has an overdue loan and cannot loan a new book.')
        return jsonify({'error': 'You have an overdue loan and cannot loan a new book until it is returned.'}), 400

    # Get the book details
    book = Book.query.get(book_id)
    if not book:
        app.logger.error(f'Book with ID {book_id} not found')
        return jsonify({'error': 'Book not found'}), 404

    # Check if the book is already loaned out
    if book.amount < 1:
        app.logger.warning(f'No available copies of book {book_id}')
        return jsonify({'error': 'No available copies of this book.'}), 400

    # Calculate the return date by adding the book's loan date (in days) to today's date
    return_date = datetime.utcnow() + timedelta(days=book.loandate)

    # Create new loan
    loan = Loan(user_id=user_id, book_id=book_id, return_date=return_date)
    db.session.add(loan)
    db.session.commit()

    app.logger.info(f'Book {book_id} loaned successfully to user {user_id}, return date: {return_date.strftime("%Y-%m-%d %H:%M:%S")}')
    
    return jsonify({'message': 'Book loaned successfully', 'return_date': return_date.strftime('%Y-%m-%d %H:%M:%S')}), 200

#get all lons for a specific user, took fucking forever beacuse i accidently used caps
@app.route('/api/user-loans/<int:user_id>', methods=['GET'])
def get_user_loans(user_id):
    app.logger.info(f'Fetching loans for user with ID: {user_id}')
    
    loans = Loan.query.filter_by(user_id=user_id).all()

    if not loans:
        app.logger.warning(f'No loans found for user with ID: {user_id}')
        return jsonify({'message': 'No loans found for this user'}), 404
    
    loan_data = [
        {
            'id': loan.id,
            'book': {
                'name': loan.book.name
            },
            'loan_date': loan.loan_date,
            'return_date': loan.return_date
        }
        for loan in loans
    ]
    
    app.logger.info(f'Retrieved {len(loans)} loans for user with ID: {user_id}')
    
    return jsonify(loan_data)

@app.route('/api/delete-loan/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    app.logger.info(f'Attempting to delete loan with ID: {loan_id}')
    
    loan = Loan.query.get(loan_id)
    
    if loan:
        try:
            db.session.delete(loan)
            db.session.commit()
            app.logger.info(f'Loan with ID {loan_id} deleted successfully')
            return jsonify({'message': 'Loan deleted successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error deleting loan with ID {loan_id}: {str(e)}')
            return jsonify({'error': 'An error occurred while deleting the loan.'}), 500
    else:
        app.logger.warning(f'Loan with ID {loan_id} not found')
        return jsonify({'error': 'Loan not found.'}), 404

@app.route('/api/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Log the attempt to update the user
    app.logger.info(f'Attempting to update user with ID: {user_id}')
    
    user = User.query.get_or_404(user_id)  # Get the user, or return 404 if not found
    data = request.get_json()  # Get the data from the request

    # Validate input
    name = data.get('name')
    email = data.get('email')

    if not name and not email:
        app.logger.warning('At least one field (name or email) must be provided to update')
        return jsonify({'error': 'At least one field (name or email) must be provided to update'}), 400

    # Update fields if provided
    if name:
        app.logger.info(f'Updating name to {name}')
        user.name = name
    if email:
        # Check if the new email is already in use by another user
        existing_user = User.query.filter(User.email == email, User.id != user_id).first()
        if existing_user:
            app.logger.warning(f'Email {email} already in use by another user')
            return jsonify({'error': 'Email already in use by another user'}), 400
        app.logger.info(f'Updating email to {email}')
        user.email = email

    try:
        db.session.commit()  # Save the changes to the database
        app.logger.info(f'User with ID {user_id} updated successfully')
        return jsonify({'message': 'User updated successfully', 'user': user.to_dict()}), 200
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        
        # Log the error
        app.logger.error(f'Error updating user with ID {user_id}: {str(e)}')
        
        return jsonify({'error': 'Failed to update user', 'details': str(e)}), 500


# Flask route to update a book
@app.route('/api/update-book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    # Log the incoming request
    app.logger.info(f'Attempting to update book with ID: {book_id}')
    
    # Get the data from the request
    data = request.get_json()

    # Extract data from the request
    updated_name = data.get('name')
    updated_author = data.get('author')
    updated_genre = data.get('genre')
    updated_year = data.get('year')

    # Validate the data
    if not updated_name or not updated_author or not updated_genre or not updated_year:
        app.logger.warning('Missing required fields in request data')
        return jsonify({'error': 'All fields are required'}), 400

    try:
        # Find the book by ID
        book = Book.query.get(book_id)

        if not book:
            app.logger.warning(f'Book with ID {book_id} not found')
            return jsonify({'error': 'Book not found'}), 404

        # Log the old book data
        app.logger.info(f'Found book: {book.name}, {book.author}, {book.genre}, {book.year}')

        # Update the book's attributes
        book.name = updated_name
        book.author = updated_author
        book.genre = updated_genre
        book.year = updated_year

        # Commit the changes to the database
        db.session.commit()

        # Log the successful update
        app.logger.info(f'Book with ID {book_id} updated successfully')

        return jsonify({'message': 'Book updated successfully'}), 200

    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        
        # Log the error
        app.logger.error(f'Error updating book with ID {book_id}: {str(e)}')
        
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    app.logger.info('Fetching all users from the database')
    users = User.query.all()  # Fetch all users from the database
    users_data = [
        {"id": user.id, "name": user.name, "email": user.email} for user in users
    ]
    return jsonify(users_data)

if __name__ == '__main__':
    # Initialize the database
    with app.app_context():
        db.create_all()

    app.run(debug=True)
