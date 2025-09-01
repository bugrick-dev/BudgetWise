from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from helpers import login_required, usd

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budgetwise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Session(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False) #user adds categories
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    account_name = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300))
    transaction_date = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template("index.html", user=user)

        
@app.route("/signup", methods=["GET", "POST"])
def signup():

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not password or not confirm_password:
            return render_template("signup.html", error="All fields are required")
        
        if User.query.filter_by(username=username).first():
            return render_template("signup.html", error="Username already exists")

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password_hash=hashed_password) # pyright: ignore[reportCallIssue]
        db.session.add(new_user)
        db.session.commit()


        return redirect(url_for("index"))
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="All fields are required")

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password_hash, password):
            return render_template("login.html", error="Invalid username or password")

        session["user_id"] = user.id
        session["username"] = user.username

        return redirect(url_for('index'))
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings(): #TODO

    if request.method == "POST":

        new_username = request.form.get("username")
        current_password = request.form.get("old-password")
        new_password = request.form.get("new-password")
        new_category = request.form.get("new-category")

        user = User.query.filter_by(id=session.get("user_id")).first()


        if new_category:
            add_category = Category(name=new_category)
            db.session.add(add_category)

        change_flag = False

        if check_password_hash(user.password_hash, current_password):
            if current_password == new_password:
                user.password_hash = generate_password_hash(new_password)
                change_flag = True

        if new_username:
            user.username = new_username
            change_flag = True

        if change_flag:
            db.session.commit()
            session.clear()

        flash("Changes Saved!")
        return redirect(url_for("index"))

    return render_template("settings.html")





@app.route("/delete_user", methods=["POST"])
@login_required
def delete_user():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            session.clear()
            return redirect(url_for("index"))
    return redirect(url_for("settings"))

@app.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")

@app.route("/accounts")
@login_required
def accounts():
    user_id = session.get("user_id")
    accounts = Account.query.filter_by(user_id=user_id).all()
    return render_template("accounts.html", accounts=accounts)

@app.route("/add_account", methods=["POST"])
@login_required
def add_account():
    account_name = request.form.get("account_name")
    balance = request.form.get("balance", type=float, default=0.0)
    user_id = session.get("user_id")
    if not account_name:
        flash("Account name is required", "danger")
        return redirect(url_for("accounts"))
    if Account.query.filter_by(user_id=user_id, account_name=account_name).first():
        flash("Account with this name already exists", "danger")
        return redirect(url_for("accounts"))
    new_account = Account(user_id=user_id, account_name=account_name, balance=balance) # pyright: ignore[reportCallIssue]
    db.session.add(new_account)
    db.session.commit()
    flash("Account Added Successfully", "success")
    return redirect(url_for("accounts"))

@app.route("/delete_account/<int:account_id>", methods=["GET","POST"])
@login_required
def delete_account(account_id):
    user_id = session.get("user_id")
    account = Account.query.filter_by(id=account_id, user_id=user_id).first()
    if account:
        db.session.delete(account)
        db.session.commit()
        flash("Account Deleted Successfully", "success")
        return redirect(url_for("accounts"))  
    flash("Account Delete Error", "danger")
    return redirect(url_for("accounts"))

def init_db():
    db.create_all()
    return

if __name__ == "__main__":
    app.run(debug=True)