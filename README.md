# primotech_api
Not official api for mobile application to server

IF DATABASE OR COLUMN CHANGED TO RUN THE MIGRATIONS
BY RUNNING THE MIGRATION YOU SHOULD RUN IT IN TERMINAL

> alembic revision --autogenerate -m "name of commit"

NOTE:
    YOU SHOULD MODIFY THE method upgrade... (IT DELETES OR DROP THE COLUMN!!!!!!!!!!!)
    THEN RUN THIS CODE

>alembic upgrade head

