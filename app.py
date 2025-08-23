from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budgetwise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Session(app)

@app.route("/")
def index():
    return render_template("index.html", session=session)


        
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not password or not confirm_password:
            return "All fields are required", 400

        if password != confirm_password:
            return "Passwords do not match", 400

        hashed_password = generate_password_hash(password)

        # Here you would typically save the user to a database
        # For demonstration, we'll just store it in the session
        session["user"] = {"username": username, "password": hashed_password}

        return redirect(url_for("index"))
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)