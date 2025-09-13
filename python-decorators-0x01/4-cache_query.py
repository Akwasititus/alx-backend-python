#!/usr/bin/env python3
"""
Task 4: Cache Database Queries
Implements a decorator `cache_query` to cache query results
based on the SQL query string to avoid redundant database calls.
"""

import time
import sqlite3
import functools

# In-memory cache: {query_string: result}
query_cache = {}


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


def cache_query(func):
    """
    Decorator that caches the results of a database query
    using the SQL query string as the cache key.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract the SQL query: look for 'query' kwarg or first positional arg
        query = kwargs.get("query")
        if query is None and args:
            query = args[0]

        # Check cache
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing and caching result for query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from the database, caching results by query string.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will hit the database and cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call:", users)

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call (from cache):", users_again)
    assert users == users_again, "Cached result should match the original result"