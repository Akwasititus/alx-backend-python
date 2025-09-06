#!/usr/bin/python3
"""
Memory-Efficient Aggregation with Generators
Calculate average age without loading entire dataset into memory.
"""

import sqlite3
import os


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    
    Yields:
        int: Age of a user
    """
    db_path = 'ALX_prodev.db'
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file {db_path} not found. Please run seed.py first.")
    
    connection = sqlite3.connect(db_path)
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # First loop: fetch ages one by one
        row = cursor.fetchone()
        while row is not None:
            yield row[0]  # Yield the age
            row = cursor.fetchone()
            
    finally:
        connection.close()


def calculate_average_age():
    """
    Calculates the average age of users using the generator.
    Uses memory-efficient approach without loading all data at once.
    
    Returns:
        float: Average age of users
    """
    total_age = 0
    count = 0
    
    # Second loop: iterate through ages from generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0  # Avoid division by zero
    
    return total_age / count


if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")