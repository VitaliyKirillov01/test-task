from locust import task, HttpUser, between
import random

# A list of data payloads for the POST requests
POST_DATA = [
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss"},
    {"title": "The Secret History", "author": "Donna Tartt"},
    {"title": "Sapiens", "author": "Yuval Noah Harari"},
    {"title": "Educated", "author": "Tara Westover"},
    {"title": "Where the Crawdads Sing", "author": "Delia Owens"},
]


class ApiUser(HttpUser):
    wait_time = between(1, 2.5)

    host = "http://127.0.0.1:5000"

    # --- Tasks ---

    @task(3)  # The number in parentheses is the "weight" (how often this task runs relative to others)
    def get_all_books(self):
        """Simulates a user requesting the list of all books (GET /books)."""
        # The 'self.client' is the HTTP client provided by Locust
        self.client.get("/books", name="/books [GET all]")
        # 'name' is used to group similar requests in the Locust report

    @task(2)
    def get_single_book(self):
        """Simulates a user requesting a single book by ID (GET /books/id)."""
        # Since the API starts with IDs 1 and 2, we simulate requesting one of those
        book_id = random.randint(1, 2)
        self.client.get(f"/books/{book_id}", name="/books/[id] [GET single]")

    @task(1)
    def post_new_book(self):
        """Simulates a user creating a new book (POST /books)."""
        # Select a random book payload from the list
        data = random.choice(POST_DATA)

        # Send the POST request with the JSON payload
        self.client.post("/books", json=data, name="/books [POST new]")
