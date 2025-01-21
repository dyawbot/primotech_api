import mysql.connector
from mysql.connector import Error

def connect_to_database():
    connection = None  # Ensure the variable is defined even before connecting
    try:
        # Database connection parameters
        connection = mysql.connector.connect(
            host="localhost",        # Replace with your MySQL host
            user="root",             # Replace with your MySQL username
            password="",             # Replace with your MySQL password
            database="db_primo_tech" # Replace with your database name
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()
            
            # Example: Execute a query
            query = "SELECT DATABASE();"  # Simple query to check the current database
            cursor.execute(query)
            
            # Fetch the result
            record = cursor.fetchone()
            print(f"Connected to database: {record[0]}")
            
            # Close the cursor
            cursor.close()
    
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    
    finally:
        # Ensure the connection is closed if it was successfully opened
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

# Call the function to connect
connect_to_database()
