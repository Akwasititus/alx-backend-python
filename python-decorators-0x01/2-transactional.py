#!/usr/bin/env python3
"""
Task 2: Transaction Management Decorator
Ensures a database operation is executed inside a transaction.
Commits if successful; rolls back on any exception.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Opens a SQLite connection to users.db, passes it to the
    decorated function as the first argument, and ensures
    the connection is closed afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def transactional(func):
    """
    Decorator to wrap a function call inside a database transaction.
    If the wrapped function raises an exception, the transaction is rolled back;
    otherwise the transaction is committed.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update the email of a user given their ID.
    Automatically runs inside a transaction.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )


if __name__ == "__main__":
    # Update user's email with automatic transaction handling
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
    print("User email updated successfully.")

