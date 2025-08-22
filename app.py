from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)