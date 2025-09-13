#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager

A custom context manager ExecuteQuery that:
- connects to a SQLite database,
- executes a provided SQL query with parameters,
- returns the results,
- and ensures the connection closes automatically.
"""

import sqlite3


class ExecuteQuery:
    """
    Context manager for executing a SQL query with parameters.
    Usage:
        with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (25,)) as rows:
            for row in rows:
                print(row)
    """

    def __init__(self, db_name: str, query: str, params: tuple = ()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """
        Opens the database connection, executes the query,
        fetches all results, and returns them.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensures cursor and connection are closed.
        Rolls back if an exception occurred.
        """
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        # Returning False allows exceptions to propagate if needed
        return False


if __name__ == "__main__":
    # Example usage
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery("users.db", query, params) as results:
        for row in results:
            print(row)
    print("Query executed and connection closed successfully.")
    # Connection is automatically closed here