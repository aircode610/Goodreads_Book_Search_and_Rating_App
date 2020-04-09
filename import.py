import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    books_file = open("books.csv")
    rows = csv.reader(books_file)
    count = 1
    for isbn, title, author, year in rows:
        if count == 1:
            count += 1
            continue
        else:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()
if __name__ == "__main__":
    main()
