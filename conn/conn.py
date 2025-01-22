from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:unknownpass@192.168.56.101:5432/postgres"


# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Test connection
try:
    with engine.connect() as connection:
        print("Connected to PostgreSQL!")
except Exception as e:
    print(f"Connection failed: {e}")
