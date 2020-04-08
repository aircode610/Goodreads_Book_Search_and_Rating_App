import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if session.get("user_id") is None:
        return render_template("index.html")
    else:
        return redirect(url_for("home"))
@app.route("/sign-up")
def signup():
    return render_template("sign-up.html")
@app.route("/log-in")
def login():
    return render_template("log-in.html")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    all_users = db.execute("SELECT username, password FROM users").fetchall()
    for user, pwd in all_users:
        if user == username:
            return render_template("sign-up-wrong.html", message="This username has already been taken!")
    if password == confirm:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",{"username": username, "password": password})
        id = db.execute("SELECT id FROM users WHERE username = :username", {"username" : username}).fetchone()
        session["user_id"] = id
        db.commit()
        return redirect(url_for("home"))
    else:
        return render_template("sign-up-wrong.html", message="The passwords you typed in do not match!")
@app.route("/login-check", methods=["POST"])
def login_check():
    username = request.form.get("username")
    password = request.form.get("password")
    all_users = db.execute("SELECT username, password FROM users").fetchall()
    for user, pwd in all_users:
        if user == username and pwd == password:
            id = db.execute("SELECT id FROM users WHERE username = :username", {"username" : username}).fetchone()
            session["user_id"] = id
            db.commit()
            return redirect(url_for("home"))
    return render_template("login-wrong.html")
@app.route("/log-out")
def log_out():
    session["user_id"] = None
    return redirect(url_for("index"))
