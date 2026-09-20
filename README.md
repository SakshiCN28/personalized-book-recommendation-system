# 📚 Personalized Book Recommendation System

A web-based **Personalized Book Recommendation System** developed using **Python and Django**.

The system allows users to browse books, search and filter books by genre, rate books, save favorite books, and receive personalized recommendations based on their interests and activities.

---

## ✨ Features

- 👤 User Registration
- 🔐 User Login and Logout
- 📚 Browse Books
- 🔎 Search Books
- 🏷️ Filter Books by Genre
- ⭐ Rate Books
- ❤️ Add Books to Favorites
- 👤 User Profile
- 📊 Personalized User Dashboard
- 🤖 Personalized Book Recommendations
- 📖 Detailed Book Information
- 🌐 Book Cover Images

---

## 🤖 Recommendation System

The system uses a simple **rule-based recommendation algorithm**.

A recommendation score is calculated for each book based on the user's preferences and activities.

| Recommendation Factor | Score |
|---|---:|
| Favorite genre matches the book | +3 |
| User rated the book 4 or 5 | +2 |
| User added the book to favorites | +2 |
| Overall book rating × 0.2 | Additional score |

Books are then sorted according to their recommendation score.

### Example

If a user's favorite genre is **Fiction** and they have rated a Fiction book highly and added it to their favorites, that book receives additional recommendation points.

Higher score → Higher recommendation priority.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Django | Web Framework |
| HTML | Frontend Structure |
| CSS | Website Styling |
| SQLite | Database |
| VS Code | Development Environment |
| OpenLibrary | Book Cover Images |

---

## 🏗️ Project Structure

```text
BookRecommendationSystem/
│
├── bookrecommendation/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── books/
│   ├── migrations/
│   ├── templates/
│   │   └── books/
│   │       ├── book_list.html
│   │       ├── book_detail.html
│   │       ├── dashboard.html
│   │       ├── favorites.html
│   │       ├── login.html
│   │       ├── register.html
│   │       └── profile.html
│   │
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── db.sqlite3
├── manage.py
└── README.md


## 📂 How to Run
1. Open VS Code
2. Open folder C:\Users\SAKSHI C.N\OneDrive\Desktop\BookRecommendationSystem
3. Open the terminal and in terminal you should C:\Users\SAKSHI C.N\OneDrive\Desktop\BookRecommendationSystem 
4. venv\Scripts\activate (To Activate your virtual environment, should type this in terminal)
5. python manage.py runserver (Start Django)
6. Open Chrome/Edge and search for 'http://127.0.0.1:8000/'
7. To register: 'http://127.0.0.1:8000/register/'
8. To login: 'http://127.0.0.1:8000/login/'
9.  Or simply step 6


## 👨‍💻 Author
SAKSHI CN
