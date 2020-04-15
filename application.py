import os
import requests
import math

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
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
    return render_template("sign-up.html", message="")


@app.route("/log-in")
def login():
    return render_template("log-in.html", message="")


@app.route("/home")
def home():
    if session.get("user_id") is None:
        return render_template("index.html")
    else:
        return render_template("home.html", result="home")


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    all_users = db.execute("SELECT username, password FROM users").fetchall()
    if username == "" or password == "" or confirm == "":
        return render_template("sign-up.html", message="You need to fill all of the inputs!")
    for user, pwd in all_users:
        if user == username:
            return render_template("sign-up.html", message="This username has already been taken!")
    if password == confirm:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",{"username": username, "password": password})
        id = db.execute("SELECT id FROM users WHERE username = :username", {"username" : username}).fetchone()
        session["user_id"] = id
        db.commit()
        return redirect(url_for("home"))
    else:
        return render_template("sign-up.html", message="The passwords you typed in do not match!")


@app.route("/login-check", methods=["POST"])
def login_check():
    username = request.form.get("username")
    password = request.form.get("password")
    all_users = db.execute("SELECT username, password FROM users").fetchall()
    if username == "" or password == "":
        return render_template("log-in.html", message="You need to fill all of the inputs!")
    for user, pwd in all_users:
        if user == username and pwd == password:
            id = db.execute("SELECT id FROM users WHERE username = :username", {"username" : username}).fetchone()
            session["user_id"] = id
            db.commit()
            return redirect(url_for("home"))
    return render_template("log-in.html", message="The username or password that you entered is invalid!")

@app.route("/log-out")
def log_out():
    session["user_id"] = None
    return redirect(url_for("index"))
@app.route("/search", methods=["GET"])
def search():
    string = str(request.args.get("keyword")).lower()
    results = []
    all_books = db.execute("SELECT isbn, title, author FROM books").fetchall()
    for isbn, title, author in all_books:
        if string in isbn.lower() or string in title.lower() or string in author.lower():
            results.append([isbn, title, author])
    db.commit()
    return render_template("home.html", result=results)


@app.route("/book/<book_title>")
def book(book_title):

    book_title = book_title
    book_info = db.execute("SELECT id, isbn, title, author, year FROM books WHERE title = :title", {"title": book_title}).fetchone()
    isbn = book_info['isbn']

    # handle error; what if there is no goodreads review?
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "GhLOXmdJzO0kf2gDtsXg", "isbns": isbn})
    ai = res.json()["books"][0]
    rating = ai["average_rating"]
    rating_count = ai["work_ratings_count"]
    good_reads_rating = {}
    good_reads_rating['rating'] = float(rating)
    good_reads_rating['rating_count'] = float(rating_count)
    good_reads_rating['rating_truncated'] = math.trunc(float(rating))


    review_info = []
    reviews = db.execute("SELECT review_text, rating, username FROM reviews JOIN users ON reviews.user_id = users.id WHERE reviews.book_id = :id", {"id": book_info['id']}).fetchall()
    for elem in reviews:
        review_info.append(elem)

    return render_template("book.html", book_info=book_info, good_reads_rating=good_reads_rating, review=review_info)


@app.route("/api/<isbn>")
def books_api(isbn):
    info = []
    book_info = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book_info == None:
        return jsonify({"error":"Invalid isbn"}), 404
    for i in book_info:
        info.append(i)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "GhLOXmdJzO0kf2gDtsXg", "isbns": info[0]})
    ai = res.json()["books"][0]
    return jsonify({
        "title": info[1],
        "author": info[2],
        "year": info[3],
        "isbn": info[0],
        "review_count": int(ai["work_ratings_count"]),
        "average_score": float(ai["average_rating"])
    })
@app.route("/review/<title>")
def review_page(title):
    author = db.execute("SELECT author FROM books WHERE title = :title", {"title" : title}).fetchone()[0]
    return render_template("review.html", t=title, a=author, message="")
@app.route("/sending/<t>", methods=["GET"])
def review(t):
    rating = request.args.get("rate")
    review = str(request.args.get("review"))
    user_id = session["user_id"][0]
    book_id = db.execute("SELECT id FROM books WHERE title = :title", {"title" : t}).fetchone()[0]
    check = db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id = users.id WHERE user_id = :user_id AND book_id = :book_id", {"user_id" : user_id, "book_id" : book_id}).fetchone()
    info = []
    book_info = db.execute("SELECT id, isbn, title, author, year FROM books WHERE title = :title", {"title": t}).fetchone()
    count = 0
    id = 0
    isbn = db.execute("SELECT isbn FROM books WHERE title = :title", {"title": t}).fetchone()
    for i in book_info:
        if count == 0:
            id = int(i)
            count += 1
            continue
        info.append(i)
    if check == None:
        db.execute("INSERT INTO reviews (user_id, book_id, review_text, rating) VALUES (:user_id, :book_id, :review_text, :rating)",{"user_id": user_id, "book_id": book_id, "review_text": review, "rating": rating})
    else:
        return render_template("review.html",t=t, a=info[2], message="You've posted another review")
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "GhLOXmdJzO0kf2gDtsXg", "isbns": isbn})
    ai = res.json()["books"][0]
    rating = ai["average_rating"]
    rating_count = ai["work_ratings_count"]
    info.append(float(rating))
    info.append(rating_count)
    info.append(math.trunc(float(rating)))
    review_info = []
    reviews = db.execute("SELECT review_text, rating, username FROM reviews JOIN users ON reviews.user_id = users.id WHERE reviews.book_id = :id", {"id": id}).fetchall()
    for elem in reviews:
        review_info.append(elem)
    db.commit()
    return render_template("book.html", info=info, review=review_info)

