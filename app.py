from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from helpers import login_required, usd

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budgetwise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Session(app)

from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False) 
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300))
    transaction_type = db.Column(db.String(10), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


# A decorator to clear the cache after each request
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Index Route
@app.route("/")
def index():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        accounts = Account.query.filter_by(user_id=user.id).all()                   #pyright: ignore
        flag = None
        if Transaction.query.filter_by(user_id=user.id).all():                      #pyright: ignore
            flag = 1

        transactions_table = db.session.query(Account, Transaction).\
                            join(Account, Transaction.account_id == Account.id).\
                            filter(Account.user_id == user.id                   #pyright: ignore
                            ).order_by(Transaction.transaction_date.desc()).\
                            limit(5)
        
        transaction_chart = db.session.query(Category.name, db.func.sum(Transaction.amount).label("total_amount")).\
                            join(Transaction).\
                            filter(Transaction.user_id == user.id).group_by(Category.name).order_by(Category.name).all()    #pyright: ignore
                            
                            
        
        transaction_line = db.session.query(
                    db.func.strftime('%m', Transaction.transaction_date).label('month_str'),
                    db.func.sum(Transaction.amount).label('total')
                    ).filter(Transaction.user_id == user.id).group_by('month_str').all()        #pyright: ignore



        net_balance = 0

        chart_data = [{"category": name, "amount": amount} for name, amount in transaction_chart]
        lineChartData = [{"month": month, "amount": amount} for month, amount in transaction_line]

        for account in accounts:
            net_balance += account.balance

        
        print(lineChartData)
        return render_template("index.html", lineChartData=lineChartData, chart_data=chart_data, user=user, net_balance=net_balance, usd=usd, transactions=transactions_table, flag=flag)
    
    return render_template("index.html", user=user)

# SignUp Route   
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

# Login Route
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

# Logout Route
@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))

# Settings Route
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings(): 

    if request.method == "POST":

        new_username = request.form.get("username")
        current_password = request.form.get("old-password")
        new_password = request.form.get("new-password")
        change_flag = False

        user = User.query.filter_by(id=session.get("user_id")).first()

        if check_password_hash(user.password_hash, current_password): # pyright: ignore[reportOptionalMemberAccess, reportArgumentType]
            if current_password != new_password:
                user.password_hash = generate_password_hash(new_password)   # pyright: ignore[reportOptionalMemberAccess, reportArgumentType]
                change_flag = True

        if new_username:
            user.username = new_username # pyright: ignore[reportOptionalMemberAccess]
            change_flag = True

        db.session.commit()

        if change_flag:
            flash("Changes Saved!", "success")
            session.clear()

        return redirect(url_for("index"))

    return render_template("settings.html")


# Delete User Route
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


# Transactions Route
@app.route("/transactions")
@login_required
def transactions():
    user_id = session.get("user_id")
    categories = Category.query.all()
    accounts = Account.query.filter_by(user_id=user_id)
    
    sort_by = request.args.get("sort_by")

    transactions = db.session.query(Transaction, Account, Category).\
    join(Account, Transaction.account_id == Account.id).\
    join(Category, Transaction.category_id == Category.id).\
    filter(Account.user_id == user_id)


    
    if sort_by == "date_asc":
        transactions = transactions.order_by(Transaction.transaction_date.asc()).all()
        flag = 2
    elif sort_by == "category":
        transactions = transactions.order_by(Transaction.category_id.desc()).all()
        flag = 3
    elif sort_by == "amount_desc":
        transactions = transactions.order_by(Transaction.amount.desc()).all()
        flag = 4
    elif sort_by == "amount_asc":
        transactions = transactions.order_by(Transaction.amount.asc()).all()
        flag = 5
    elif sort_by == "account":
        transactions = transactions.order_by(Transaction.account_id.desc()).all()
        flag = 6
    elif sort_by == "type":
        transactions = transactions.order_by(Transaction.transaction_type).all()
        flag = 7
    else:
       transactions = transactions.order_by(Transaction.transaction_date.desc()).all()
       flag = 1
    
    return render_template("transactions.html",accounts=accounts, categories=categories, transactions=transactions, usd=usd, url_for=url_for, flag=flag)

# Adding a Transaction Route
@app.route("/add_transaction", methods=["POST"])
@login_required
def add_transaction():
    user_id = session.get("user_id")
    date = request.form.get("date")
    if date:
        transaction_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        transaction_date = datetime.now()
    desc = request.form.get("description")
    amount = request.form.get("amount", type=float)
    account_id = request.form.get("account_id", type=int)
    transaction_type = request.form.get("transaction_type")
    category_id = request.form.get("category", type=int)
    try:
        account = Account.query.filter_by(id=account_id).first()
        


        new_transaction = Transaction(user_id=user_id,                  #pyright: ignore
                                    account_id=account_id,              #pyright: ignore    
                                    amount=amount,                      #pyright: ignore    
                                    description=desc,                   #pyright: ignore
                                    transaction_type=transaction_type,  #pyright: ignore    
                                    transaction_date=transaction_date,  #pyright: ignore
                                    category_id=category_id)            #pyright: ignore

        
        if transaction_type == "income":
            account.balance += amount                                   #pyright: ignore
        else:   
            account.balance -= amount                                   #pyright: ignore
        
        db.session.add(new_transaction)
        db.session.commit()
        flash("Transaction Added!", "success")
    except Exception as e:
        flash(f"An Error Occurred {e}", "danger")
        db.session.rollback()
    
    return redirect(url_for("transactions"))

# Accounts Route
@app.route("/accounts")
@login_required
def accounts():
    user_id = session.get("user_id")
    accounts = Account.query.filter_by(user_id=user_id).all()
    return render_template("accounts.html", accounts=accounts, usd=usd)

# Account Add Route
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

# Delete Account Route
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


# Function to initialize the database
def init_db():
    db.create_all()
    return

if __name__ == "__main__":
    app.run(debug=False)