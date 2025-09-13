#!/usr/bin/env python3
"""
Task 3: Concurrent Asynchronous Database Queries

Use aiosqlite to fetch:
1. All users
2. Users older than 40
concurrently using asyncio.gather.
"""

import asyncio
import aiosqlite


DB_NAME = "users.db"


async def async_fetch_users():
    """
    Fetch all users from the database asynchronously.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    """
    Fetch users older than 40 from the database asynchronously.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """
    Run both queries concurrently and display their results.
    """
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("=== All Users ===")
    for user in all_users:
        print(user)

    print("\n=== Users Older Than 40 ===")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    # Launch the concurrent fetch operations
    asyncio.run(fetch_concurrently())
    print("Concurrent fetch operations completed successfully.")
    # All connections are automatically closed here