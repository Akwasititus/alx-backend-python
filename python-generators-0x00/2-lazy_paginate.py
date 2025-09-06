#!/usr/bin/python3
"""
Lazy loading paginated data - simulates fetching paginated data using a generator.
"""

import sqlite3
import os


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database.
    
    Args:
        page_size (int): Number of records to fetch
        offset (int): Starting position for the records
        
    Returns:
        list: A list of user records as dictionaries
    """
    db_path = 'ALX_prodev.db'
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file {db_path} not found. Please run seed.py first.")
    
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        return [dict(row) for row in rows]
    finally:
        connection.close()


def lazy_pagination(page_size):
    """
    Generator that lazily loads paginated data from the database.
    
    Args:
        page_size (int): Number of records per page
        
    Yields:
        list: A page of user records as dictionaries
    """
    offset = 0
    
    # Single loop as required
    while True:
        # Fetch the next page
        page = paginate_users(page_size, offset)
        
        # If no more records, break the loop
        if not page:
            break
        
        # Yield the page
        yield page
        
        # Update offset for next page
        offset += page_size


if __name__ == "__main__":
    # Test the lazy pagination
    print("Testing lazy pagination (page size: 5):")
    
    page_count = 0
    for page in lazy_pagination(5):
        print(f"\nPage {page_count + 1}:")
        for user in page:
            print(user)
        
        page_count += 1
        if page_count >= 3:  # Show only first 3 pages for testing
            break