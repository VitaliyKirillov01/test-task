from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {'id': 1, 'title': 'The Hitchhiker\'s Guide to the Galaxy', 'author': 'Douglas Adams'},
    {'id': 2, 'title': 'Pride and Prejudice', 'author': 'Jane Austen'}
]
next_id = 3


# GET all books
@app.route('/books', methods=['GET'])
def get_books():
    """Returns a list of all books."""
    # jsonify converts the Python dictionary/list into a JSON response
    return jsonify(books)


# GET single book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Returns a single book based on its ID."""
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    # Return a 404 Not Found error if the book doesn't exist
    return jsonify({'error': 'Book not found'}), 404


# 3. POST (Create) a new book
@app.route('/books', methods=['POST'])
def add_book():
    """Adds a new book to the list."""

    data = request.get_json()

    if not data or 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Missing title or author'}), 400  # Bad Request

    global next_id
    new_book = {
        'id': next_id,
        'title': data['title'],
        'author': data['author']
    }
    books.append(new_book)
    next_id += 1

    return jsonify(new_book), 201


if __name__ == '__main__':
    app.run(debug=True)
