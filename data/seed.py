import os
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

# Database credentials from environment variables
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "pass123")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ideas")

# Create the database engine
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL)

users = [
    {
        "name": "Alice",
        "email": "alice@gmail.com",
        "password": "password123"
    },
    {
        "name": "Bob",
        "email": "bob@gmail.com",
        "password": "password123"
    },
    {
        "name": "Charlie",
        "email": "charlie@gmail.com",
        "password": "password123"
    },
    {
        "name": "Diana",
        "email": "diana@gmail.com",
        "password": "password123"
    },
    {
        "name": "Eve",
        "email": "eve@gmail.com",
        "password": "password123"
    },
    {
        "name": "Frank",
        "email": "frank@gmail.com",
        "password": "password123"
    }
]

try:
    # Connect to the database and execute the query within a transaction
    with engine.begin() as connection:

        # Insert new users
        for user in users:
            # Hash the password before storing it
            hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user["password"])
            user["password"] = hashed_password
            connection.execute(
                # FIX: Enclose "user" in double quotes because it's a reserved keyword
                text("INSERT INTO \"user\" (username, email, , role) VALUES (:username, :email, :password)"),
                {"username": user["name"], "email": user["email"], "password": user["password"], "role": "user"}
            )
        print("Users inserted successfully.")

except Exception as e:
    print(f"An error occurred: {e}")