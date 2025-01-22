import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    original_name = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {"id": self.id, "filename": self.filename, "original_name": self.original_name}


# Initialize database

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# API Routes
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        original_name = file.filename
        unique_filename = f"{uuid.uuid4().hex}_{original_name}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        # Save metadata to database
        image = Image(filename=unique_filename, original_name=original_name)
        db.session.add(image)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'filename': unique_filename}), 200

    return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif.'}), 400


@app.route('/api/images', methods=['GET'])
def list_images():
    images = Image.query.all()
    return jsonify([image.to_dict() for image in images]), 200


@app.route('/uploads/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
