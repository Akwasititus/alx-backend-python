#!/usr/bin/env python3
"""
Task 0: Logging database Queries
Create a decorator `log_queries` that logs the SQL query
executed by any decorated function.
"""

import sqlite3
import functools
from datetime import datetime


def log_queries(func):
    """
    Decorator that logs the SQL query before executing the wrapped function.
    Assumes the decorated function receives the SQL query as a `query`
    keyword argument or as the first positional argument.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Determine the query string
        query = kwargs.get("query")
        if query is None and args:
            query = args[0]
        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    """
    Connects to the users.db database and fetches all users.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Example usage
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
