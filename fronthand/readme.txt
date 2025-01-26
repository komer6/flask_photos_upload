Library Management System - Frontend README
Overview
The frontend of this project is a web application for managing books and users in a library

Folder Structure
index.html: Home page displaying the welcome message and search options for users and books.
add_user.html: Form to add a new user to the system.
add_book.html: Form to add a new book to the system.
all_users.html: Displays all users in the system.
all_books.html: Displays all books in the system.
user.html: displays a user and enables loans
styles.css: Custom styling for the app.

Setup and Installation
Clone or download the repository.
Ensure that you have the required dependencies (like Axios) included in the HTML files or installed in your project.
Open the HTML files (e.g., index.html, add_user.html) in a browser.


Library Management System - Frontend README
Overview
The frontend of this project is a web application for managing books and users in a library. It provides various features to search, view, add, edit, and delete books and users. This application interacts with a backend API (Flask) through Axios requests.

Features
Search for Users: Allows searching by user name or email.
Search for Books: Allows searching by book title, author, or year.
Manage Users: View, edit, and delete user details.
Manage Books: View, edit, and delete book details.
Navigation Bar: Easy navigation between pages like "Home", "Add User", "Add Book", "View All Users", and "View All Books".
Responsive Design: The application is designed to be responsive and works well on both desktop and mobile devices.
Folder Structure
index.html: Home page displaying the welcome message and search options for users and books.
add_user.html: Form to add a new user to the system.
add_book.html: Form to add a new book to the system.
all_users.html: Displays all users in the system.
all_books.html: Displays all books in the system.
styles.css: Custom styling for the app.
script.js: Contains JavaScript functions for managing users and books, handling form submissions, and making Axios requests to the backend API.
Setup and Installation
Clone or download the repository.
Ensure that you have the required dependencies (like Axios) included in the HTML files or installed in your project.
Open the HTML files (e.g., index.html, add_user.html) in a browser.
Axios API Integration
The frontend uses Axios to interact with the backend API. The following endpoints are used:

Search Users: GET http://127.0.0.1:5000/api/search-users?name=<searchTerm> or GET http://127.0.0.1:5000/api/search-users?email=<searchTerm>
Search Books: GET http://127.0.0.1:5000/api/search-books?title=<searchTerm>, GET http://127.0.0.1:5000/api/search-books?author=<searchTerm>, or GET http://127.0.0.1:5000/api/search-books?year=<searchTerm>
Manage User: PUT http://127.0.0.1:5000/api/update-user/<userId>
Delete User: DELETE http://127.0.0.1:5000/api/users/<userId>
Manage Book: PUT http://127.0.0.1:5000/api/update-book/<bookId>
Delete Book: DELETE http://127.0.0.1:5000/api/books/<bookId>


INDEX PAGE - Functionality
User Search
Purpose: Allows administrators to search for users by their name or email.
Features:
Search Fields:
Name: Enter the user's name to search.
Email: Enter the user's email to search.
Search Button: Submitting the search filters the user list based on the entered criteria.
Display Results: A table is dynamically updated with user information (name, email).
Actions:
Manage User: Provides options to edit user details (name, email).
Delete User: Allows the removal of a user from the system.
Book Search
Purpose: Allows users to search for books by title, author, or year.
Features:
Search Fields:
Title: Enter the book’s title.
Author: Enter the book’s author.
Year: Enter the year of publication.
Search Button: Submitting the search filters the book list based on the entered criteria.
Display Results: A table is dynamically updated with book details (title, author, genre, year, etc.).
Actions:
Manage Book: Provides options to edit book details (title, author, genre, year, etc.).
Delete Book: Allows the removal of a book from the system.
Manage User
Purpose: Provides an interface to edit user details such as name and email.
Features:
Edit Fields:
Name: Modify the user’s name.
Email: Modify the user’s email.
Actions:
Save Changes: Save the modifications made to the user’s details.
Cancel: Discard the changes and revert to the original details.
Manage Book
Purpose: Provides an interface to edit book details such as title, author, genre, and year.
Features:
Edit Fields:
Title: Modify the book’s title.
Author: Modify the book’s author.
Genre: Modify the book’s genre.
Year: Modify the book’s year of publication.
Actions:
Save Changes: Save the modifications made to the book’s details.
Cancel: Discard the changes and revert to the original details.
Deleting Users and Books
Purpose: Allows the deletion of users or books from the system.
Features:
Delete User: Removes the user from the database and updates the displayed list of users.
Delete Book: Removes the book from the database and updates the displayed list of books.
Confirmation: Before deletion, a confirmation dialog ensures the user wants to proceed with the deletion.
ADD_BOOK PAGE - Functionality
Uploading a Book
Users can upload a book by providing the following details:

ADD_BOOK - Functionality
Book Name: Title of the book.
Input Field: Text field for the book’s title.
Author: Name of the author.
Input Field: Text field for the author’s name.
Genre: The genre or category of the book (e.g., Fiction, Non-fiction, Science Fiction, etc.).
Input Field: Text field for the genre.
Year: Year of publication.
Input Field: Number field for the publication year.
Amount: The number of copies available.
Input Field: Number field for the number of copies.
Loan Date: Duration of the loan in days.
Input Field: Number field for loan duration in days.
Upload Book Cover Image
Purpose: Allows users to upload an image for the book’s cover.
Input Field: File input to select an image (accepts image files only).
Image Storage: The uploaded image is stored in the server’s uploads directory, and its filename is associated with the book.
Form Submission
Submit Button: Submitting the form triggers the backend to process the book upload, including saving metadata (name, author, genre, etc.) and the image file.
Success Message: After successful submission, a message confirms that the book has been uploaded.
Error Handling: If an error occurs, an appropriate message is shown to the user.


ADD_USER PAGE - Functionality
Adding a User
Users can add a new user to the system by providing the following details:

Name: The name of the user.
Input Field: Text field where the user can enter their name.
Email: The email address of the user.
Input Field: Email field where the user enters their email address. This ensures proper email format validation.
Form Submission
Submit Button: Once the user fills in the name and email fields, they can click the "Add User" button to submit the form.
Request: The form sends a POST request to the backend (http://127.0.0.1:5000/api/add-user) with the user's name and email as JSON data.
Success Response:
If the request is successful, a success message is displayed in the responseMessage div, indicating that the user was added successfully.
The form fields are cleared after submission.
Error Handling
Error Message: If there is an error during the form submission (e.g., missing or invalid data), an error message is displayed in the responseMessage div.
Display of Error: If the backend returns an error message (e.g., email already exists), it is displayed in the response message div.
Styling for Response Messages
Success: If the user is successfully added, the message is displayed with a success style.
Error: If an error occurs, the message is displayed with an error style.
Navigation
Navbar: The page includes a navigation bar with links to the home page, add user page, add book page, and pages for viewing all users and all books.

View All Books Page - Functionality
Displaying All Books
The View All Books page shows a list of all the books in the system. Here's how it works:

Table Display: The books are displayed in a table with columns for:
Title: The name of the book.
Author: The author of the book.
Genre: The genre of the book.
Year: The publication year of the book.
Image: A thumbnail image of the book cover.
Actions: Two actions for each book:
Manage: Allows the user to edit the book details.
Delete: Deletes the book from the system.
Fetching Book Data
The page loads all books by making an API call to http://127.0.0.1:5000/api/books using Axios.
If books are found, they are displayed in a table.
If no books are found, a message No books found is shown.
Book Management (Edit)
When the Manage button is clicked:
The book's current details are retrieved from the table and replaced with editable fields.
The user can modify the title, author, genre, and year of the book.
The book image is not editable but is displayed as a thumbnail.
A Save button allows the user to save the changes.
A Cancel button allows the user to revert the changes.
Saving Book Changes
When the Save button is clicked:
A PUT request is made to the server (http://127.0.0.1:5000/api/update-book/{bookId}) with the updated book details.
If the update is successful, a success message is shown, and the book list is refreshed to reflect the changes.
Cancelling Edits
If the Cancel button is clicked:
The form is reverted to show the original book details, and the table is restored.
Deleting a Book
When the Delete button is clicked:
A DELETE request is sent to http://127.0.0.1:5000/api/books/{bookId} to remove the book from the system.
After the book is deleted, a success message is shown, and the list of books is re-fetched.
Page Layout
The page includes a navbar with links to navigate between different pages:
Home
Add User
Add Book
View All Users
View All Books


View All Users Page - Functionality
Displaying All Users
The View All Users page shows a list of all users in the system. Here's the breakdown of its functionality:

Table Display: Users are displayed in a table with the following columns:
Name: The name of the user.
Email: The email of the user.
Actions: Includes three action buttons:
Manage: Allows the user to edit their details.
Delete: Deletes the user from the system.
View: Redirects to a user detail page (if implemented).
Fetching User Data
The page loads the list of all users by making an API call to http://127.0.0.1:5000/api/users using Axios.
If users are found, they are displayed in a table.
If no users are found, a message No users found is shown.
User Management (Edit)
When the Manage button is clicked:
The user's current details (name and email) are fetched and replaced with editable fields.
The user can modify their name and email.
After making changes, the user can either Save or Cancel.
Saving User Changes
When the Save button is clicked:
A PUT request is sent to http://127.0.0.1:5000/api/update-user/{userId} with the updated user details (name and email).
If the update is successful, the list of users is refreshed.
Cancelling Edits
If the Cancel button is clicked:
The row content is reverted to the original user details.
Deleting a User
When the Delete button is clicked:
A DELETE request is sent to http://127.0.0.1:5000/api/users/{userId} to remove the user from the system.
After the user is deleted, the list of users is refreshed.
Viewing User Details
When the View button is clicked:
The user is redirected to a page (user.html?id={userId}) to view more detailed information about that user.
Page Layout
The page includes a navbar with links to navigate between different pages:
Home
Add User
Add Book
View All Users
View All Books

User Profile Page - Functionality
Page Layout
This page is designed to display a user profile, their loan details, and a search feature for books in the library. It consists of three main sections:

User Profile Section:

Displays the user's name and email.
Fetches the user data using the user ID from the URL (?id={userId}).
User Loans Section:

Displays the user's loan history, showing:
Book name
Loan date
Return date (or "Not Returned" if the book hasn't been returned yet)
There is a Return book button next to each loan, which deletes the loan record and marks the book as returned.
Search Books Section:

Allows the user to search for books by:
Title
Author
Year
Displays a list of books matching the search query along with a Loan button to loan the selected book.
Functionality Breakdown
Fetching User Profile

The function fetchUserProfile() retrieves the user profile by making an API GET request to http://127.0.0.1:5000/api/users/{userId}, where userId is extracted from the URL (?id={userId}).
The profile data (name, email) is displayed in the User Profile section.
Viewing User Loans

The function viewLoans() retrieves all loans of the user by making an API GET request to http://127.0.0.1:5000/api/user-loans/{userId}.
The loans are listed with the loan and return dates.
The Return book button calls deleteLoan(loanId) to delete a loan, marking the book as returned.
Searching Books

The function searchBooks() performs a search based on the input value in the search box (bookSearchTerm).
The search can be performed by title, author, or year.
It makes an API GET request to http://127.0.0.1:5000/api/search-books, depending on the selected search type.
If books are found, they are displayed with their details (title, author, genre, year, and an image of the book).
Each book has a Loan button that calls loanBook(bookId) to loan the selected book.
Loaning a Book

The function loanBook(bookId) is triggered when the user clicks Loan for a book.
It sends a POST request to http://127.0.0.1:5000/api/loan-book with the user ID and the selected book ID.
Returning a Book (Deleting a Loan)

The function deleteLoan(loanId) is triggered when the user clicks Return book next to a loan.
It sends a DELETE request to http://127.0.0.1:5000/api/delete-loan/{loanId} to remove the loan record and mark the book as returned.
Page Load
When the page loads, the user profile and user loans are fetched and displayed using the fetchUserProfile() and viewLoans() functions respectively.
Error Handling
The page handles errors like missing user ID, unsuccessful API requests, and empty search results by displaying appropriate alerts or messages.

Technologies Used
HTML: For structure and content.
CSS: For styling the layout.
JavaScript: For interactivity and handling events.
Axios: For making HTTP requests to the backend API.
Backend: Flask-based API (not included in this README, but assumed to be running at http://127.0.0.1:5000).