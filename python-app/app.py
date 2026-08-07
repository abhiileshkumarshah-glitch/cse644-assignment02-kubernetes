from flask import Flask
import os

app = Flask(__name__)

DATA_FILE = "/data/persistent.txt"


@app.route("/")
def home():
    greeting = os.getenv(
        "GREETING",
        "Hello from Abhi's Python application!"
    )

    return f"""
    <html>
        <head>
            <title>CSE644 Python Application</title>
        </head>
        <body>
            <h1>{greeting}</h1>
            <h2>CSE644 - Assignment 02</h2>
            <p>Python web application running on port 8888.</p>
            <p>Application: Python Backend</p>
        </body>
    </html>
    """


@app.route("/health")
def health():
    return "healthy", 200


@app.route("/ready")
def ready():
    return "ready", 200


@app.route("/storage")
def storage():
    os.makedirs("/data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            f.write("CSE644 persistent data created by Abhi.")

    with open(DATA_FILE, "r") as f:
        data = f.read()

    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)