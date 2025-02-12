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

## 🚀 Run the Project
- **This command run in the machine or local only**
    ```sh
    uvicorn app.main:app --host localhost --port 8080



# Modified Table or Column 
- if you modified the models you need to migrate it using alembic
- *NOTE: these are only the basic command for alembic*

1. **AutoGenerate Function**
- autogenerate, generates code in the folder alembic/versions/.py
- it create two methods, **upgrade** and **downgrade**
- *NOTE: check the method for upgrade for it deletes or drop data on table and row*
    ```sh
    alembic revision --autogenerate -m "name of commit"

2. **Manual Function**
- manual function also generates code in the folder alembic/versions/.py
- the difference between the autogenerate is that you manually code the **upgrade** and **downgrade** function
    ```sh
    alembic revision -m "name of commit"

3. **Update the table**
- there are 2 ways to update the tables **upgrade** and **downgrade**
- **UPDATE**
    ```sh
    alembic upgrade head

- **DOWNGRADE**
    ```SH
    alembic downgrade head


## 📜 License
- This project is licensed under the MIT License. See LICENSE for details.