
# 📚 Goodreads Book Search and Rating App

A **Flask-based web application** that allows users to **search for books using the Goodreads API**, view details, and submit their own ratings. The project includes **user authentication**, **database integration**, and an **API for fetching book data**.

## 🚀 Features

✅ **Search Books** – Find books by title, author, or ISBN using the Goodreads API  
✅ **View Book Details** – Get information like title, author, year, and average rating  
✅ **User Authentication** – Secure **registration and login system** using hashed passwords  
✅ **Submit Ratings** – Users can rate and review books  
✅ **API Support** – Retrieve book details and user ratings through a RESTful API  
✅ **Database Integration** – Uses **PostgreSQL** with SQLAlchemy

## 🛠️ Technologies Used

- **Backend:** Flask, SQLAlchemy  
- **Database:** PostgreSQL  
- **Frontend:** HTML, CSS, Bootstrap  
- **API:** Goodreads API

## 📂 Project Structure

```
📁 Goodreads_Book_Search_and_Rating_App  
│── 📂 static/            # CSS, JS, images  
│── 📂 templates/         # HTML templates  
│── 📂 models/            # Database models  
│── 📜 app.py             # Main Flask application  
│── 📜 config.py          # Configuration settings  
│── 📜 requirements.txt   # Dependencies  
│── 📜 README.md          # Project documentation  
│── 📜 .env               # API keys (not included in repo)  
```

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/aircode610/Goodreads_Book_Search_and_Rating_App.git
cd Goodreads_Book_Search_and_Rating_App
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the root directory and add:
```
DATABASE_URL=your_postgresql_database_url
GOODREADS_API_KEY=your_goodreads_api_key
SECRET_KEY=your_secret_key
```

### 4️⃣ Initialize the Database
```bash
flask db upgrade
```

### 5️⃣ Run the Application
```bash
flask run
```
Visit **http://127.0.0.1:5000/** in your browser.

## 📡 API Endpoints

### 1️⃣ **Get Book Details**
**Endpoint:**
```
GET /api/book/<isbn>
```
**Response:**
```json
{
  "title": "Book Title",
  "author": "Author Name",
  "year": 2020,
  "isbn": "1234567890",
  "average_rating": 4.2
}
```

### 2️⃣ **Submit a Rating**
**Endpoint:**
```
POST /api/rate
```
**Request Body:**
```json
{
  "isbn": "1234567890",
  "rating": 5,
  "review": "Amazing book!"
}
```

## 🎥 Watch the YouTube Video for a Demo
You can watch the video walkthrough of this project on YouTube:  
[Goodreads Book Search and Rating App Demo](https://youtu.be/nkqNIf7mPs4)
