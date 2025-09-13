#!/usr/bin/env python3
"""
Task 1: Handle Database Connections with a Decorator
Decorator `with_db_connection` automatically opens a database
connection, passes it to the wrapped function, and closes it afterward.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Opens a SQLite connection to `users.db`, passes it to the
    decorated function as the first argument, and ensures
    the connection is closed after the function finishes.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            # Inject the connection as the first positional argument
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by their ID from the users table.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    # Fetch user by ID with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(user)
