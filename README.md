# Simple Flask API & Locust Load Test

This project demonstrates a basic RESTful API built with Flask and includes a comprehensive load testing setup using
Locust.

The goal is to provide a fully runnable example of a lightweight API and show how to stress-test it to measure
performance and stability.

## 🚀 Project Components

| Component           | Description                                                              |
|---------------------|--------------------------------------------------------------------------|
| `mock_api_books.py` | The core application: a simple Flask API for managing a list of "books." |
| `locustfile.py `    | The load testing script that simulates user traffic (GET/POST requests). |
| `README.md  `       | This document.                                                           |

## 🛠️ 1. Setup and Installation

### **Prerequisites**

You need Python 3.8+ installed on your system.

### **Install Dependencies**

Open your terminal and install the required Python libraries:

`pip install Flask locust`

## 💻 2. Running the Flask API

The API must be running before you can start the load test.

1. **Start the API:**

   Open your first terminal window and execute the Flask application:

   `python mock_api_books.py`

2. **Verify:**

   The API should start running on http://127.0.0.1:5000. Keep this terminal running for the duration of the test.

| Method | Endpoint    | Description                             |
|--------|-------------|-----------------------------------------|
| GET    | /books      | Retrieve the full list of books.        |
| GET    | /books/{id} | Retrieve a single book.                 |
| POST   | /books      | Create a new book. (Requires JSON body) |

## 3. Running the Load Test (Locust)

The Locust file (`locustfile.py`) is configured to simulate users fetching books (`GET`) and creating new books (`POST`)
against the running Flask API.

We will run Locust in headless mode to automatically execute the test for a specific duration and generate a final
report.

### Execute the Test

Open a second terminal window (while `mock_api_books.py` is still running) and execute the following command:

```
locust -f locustfile.py -H http://127.0.0.1:5000 \
-u 100 -r 10 \
--run-time 5m \
--html api_test_report.html \
--csv stats \
--headless
```

### Command Breakdown:

| Argument   | Value                 | Meaning                                            |
|------------|-----------------------|----------------------------------------------------|
| -f         | locustfile.py         | Uses the defined load test script.                 |
| -H         | http://127.0.0.1:5000 | The target API host (must match the Flask output). |
| -u         | 100                   | Total number of users to simulate.                 |
| -r         | 10                    | The spawn rate (10 users added per second).        |
| --run-time | 5m                    | The test runs for exactly 5 minutes.               |
| --html     | api_test_report.html  | The output filename for the final HTML report.     |
| --headless |                       | Runs without the web interface.                    |

### Test Completion

The test will run for 5 minutes and then automatically exit. You will see confirmation in the terminal:

```
[2025-11-21 21:50:00] Test finished: 100 users, 3000 requests, 0 failures (runtime 0:05:00)
[2025-11-21 21:50:00] Shutting down users
```

## 4. Viewing the Report

After the test completes, two files are generated in your project directory:

* `api_test_report.html`: The main, interactive load test report.

* `stats_requests.csv` and `stats_distribution.csv`: Raw data files for deeper analysis.

### How to View the Report

Simply navigate to your project directory and open the `api_test_report.html` file in any web browser.

It will contain key metrics like:

* Total Requests (RPS)

* Average Response Time

* Median Response Time

* 95th Percentile Response Time

* Failure Rate