#!/usr/bin/python3
"""
Batch processing for large data - fetches and processes users in batches.
"""

import sqlite3
import os
from contextlib import contextmanager


@contextmanager
def get_db_connection():
    """Context manager for database connection."""
    db_path = 'ALX_prodev.db'
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file {db_path} not found. Please run seed.py first.")
    
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def stream_users_in_batches(batch_size):
    """
    Generator that fetches users from the database in batches.
    
    Args:
        batch_size (int): Number of records to fetch in each batch
        
    Yields:
        list: A batch of user records as dictionaries
    """
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        
        # First loop: fetch batches until no more records
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            
            # Convert batch to list of dictionaries
            batch_dicts = [dict(row) for row in batch]
            yield batch_dicts


def batch_processing(batch_size):
    """
    Processes batches of users and filters those over age 25.
    
    Args:
        batch_size (int): Size of each batch to process
    """
    # Second loop: iterate through batches
    for batch in stream_users_in_batches(batch_size):
        # Third loop: process each user in the batch
        for user in batch:
            if user['age'] > 25:
                print(user)


if __name__ == "__main__":
    # Test the batch processing
    print("Testing batch processing (users over 25):")
    batch_processing(10)  # Use small batch size for testing