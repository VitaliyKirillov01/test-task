from locust import HttpUser, task, between, events
import random
import json

# A list of data payloads for the POST requests
POST_DATA = [
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss"},
    {"title": "The Secret History", "author": "Donna Tartt"},
    {"title": "Sapiens", "author": "Yuval Noah Harari"},
    {"title": "Educated", "author": "Tara Westover"},
]


class ApiUser(HttpUser):
    # This defines the time range a user waits between running tasks (in seconds)
    wait_time = between(1, 2.5)

    host = "http://127.0.0.1:5000"

    # --- Tasks ---

    @task(3)
    def get_all_books(self):
        """
        Simulates requesting the list of all books (GET /books)
        and validates the response structure.
        """
        response = self.client.get("/books", name="/books [GET all]")

        # Validation 1: Check HTTP Status Code
        if response.status_code != 200:
            # Report a failure if the status code is unexpected
            response.failure(f"Expected status 200, got {response.status_code}")
            return

        # Validation 2: Check JSON Content Type and structure
        try:
            # Try to parse the response as JSON
            books_list = response.json()

            # Check if the parsed object is a list (basic structure validation)
            if not isinstance(books_list, list):
                response.failure("Response content is not a JSON list.")
        except json.JSONDecodeError:
            response.failure("Response is not valid JSON.")

    @task(2)
    def get_single_book(self):
        """Simulates requesting a single book and validates the response."""
        # Use a safe ID range based on the initial state of the Flask app
        book_id = random.randint(1, 2)
        response = self.client.get(f"/books/{book_id}", name="/books/[id] [GET single]")

        if response.status_code != 200:
            response.failure(f"Expected status 200, got {response.status_code}")
            return

        try:
            book_data = response.json()

            # Check for key fields (explicit content validation)
            if 'title' not in book_data or 'author' not in book_data:
                response.failure("Book data is missing 'title' or 'author' fields.")
        except json.JSONDecodeError:
            response.failure("Response is not valid JSON.")

    @task(1)
    def post_new_book(self):
        """
        Simulates creating a new book (POST /books)
        and validates the creation status and returned ID.
        """
        data = random.choice(POST_DATA)

        response = self.client.post(
            "/books",
            json=data,
            name="/books [POST new]"
        )

        # Validation 1: Check HTTP Status Code for successful creation
        if response.status_code != 201:
            response.failure(f"Expected status 201 (Created), got {response.status_code}")
            return

        # Validation 2: Check if the response contains the new ID
        try:
            new_book = response.json()
            if 'id' not in new_book:
                response.failure("New book response is missing the 'id' field.")
        except json.JSONDecodeError:
            response.failure("Response is not valid JSON.")
