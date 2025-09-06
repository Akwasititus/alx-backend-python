#!/usr/bin/python3
"""
Generator that streams rows from SQLite database one by one.
"""

import sqlite3
import os


def stream_users():
    """
    Generator function that yields rows from user_data table one by one.
    
    Yields:
        dict: A dictionary representing a user record with keys:
              user_id, name, email, age
    """
    # Connect to the SQLite database
    db_path = 'ALX_prodev.db'
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file {db_path} not found. Please run seed.py first.")
    
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row  # This allows accessing columns by name
    
    try:
        cursor = connection.cursor()
        
        # Execute the query to get all users
        cursor.execute("SELECT * FROM user_data")
        
        # Fetch rows one by one using the generator
        row = cursor.fetchone()
        while row is not None:
            # Convert the row to a dictionary
            user_dict = {
                'user_id': row['user_id'],
                'name': row['name'],
                'email': row['email'],
                'age': row['age']
            }
            yield user_dict
            row = cursor.fetchone()
            
    finally:
        # Ensure the connection is closed even if an error occurs
        connection.close()


if __name__ == "__main__":
    # Test the generator directly
    print("Testing stream_users generator:")
    user_count = 0
    for user in stream_users():
        print(user)
        user_count += 1
        if user_count >= 5:  # Limit to 5 for testing
            break