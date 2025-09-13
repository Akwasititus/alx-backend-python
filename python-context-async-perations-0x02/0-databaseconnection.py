#!/usr/bin/env python3
"""
Task 0: Custom class-based context manager for Database connection.
Opens a SQLite database connection on entry and closes it on exit.
"""

import sqlite3


class DatabaseConnection:
    """
    Context manager that opens a SQLite database connection and
    ensures it is closed automatically, even if an exception occurs.
    """

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection and return it."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection, rolling back if an exception occurred."""
        if self.conn:
            if exc_type:
                # Roll back any uncommitted changes if an error occurs
                self.conn.rollback()
            self.conn.close()
        # Returning False lets exceptions propagate if they occurred
        return False


if __name__ == "__main__":
    # Example usage: fetch all rows from users table
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
    print("Database connection closed successfully.")
    # Connection is automatically closed here