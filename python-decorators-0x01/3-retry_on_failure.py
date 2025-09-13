#!/usr/bin/env python3
"""
Task 3: Retry Database Queries
Implements a decorator `retry_on_failure` to retry database operations
a specified number of times with a delay if an exception occurs.
"""

import time
import sqlite3
import functools


def with_db_connection(func):
    """
    Opens a SQLite connection to users.db, passes it to the
    decorated function as the first argument, and ensures
    the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """
    Decorator factory that retries a database operation up to `retries` times
    with `delay` seconds between attempts if an exception is raised.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"[Retry {attempt}/{retries}] Error: {e}")
                    if attempt < retries:
                        time.sleep(delay)
            # If all retries fail, re-raise the last exception
            raise last_exc
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the users table, retrying on transient failures.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    # Attempt to fetch users with automatic retry on failure
    users = fetch_users_with_retry()
    print(users)
    print("Users fetched successfully.")

    for user in users:
        print(user) 
    print("User details printed successfully.")
    