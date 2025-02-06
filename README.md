# primotech_api
Not official api for mobile application to server


## 🚀 Introduction
This is the API for PrimoTech, designed to handle authentication, user management, and data processing.

## 📌 Features
- User authentication (JWT-based)
- CRUD operations for users and products
- Database integration with PostgreSQL
- RESTful API with proper error handling

## 🛠️ Installation
1. **Clone the repository**:
   ```sh
   git clone https://github.com/dyawbot/primotech_api.git

IF DATABASE OR COLUMN CHANGED TO RUN THE MIGRATIONS
BY RUNNING THE MIGRATION YOU SHOULD RUN IT IN TERMINAL

> alembic revision --autogenerate -m "name of commit"

NOTE:
    YOU SHOULD MODIFY THE method upgrade... (IT DELETES OR DROP THE COLUMN!!!!!!!!!!!)
    THEN RUN THIS CODE

>alembic upgrade head

