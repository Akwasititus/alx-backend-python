#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    connection = seed.create_database(connection)
    if connection:
        connection.close()
        print(f"Database creation successful")

        connection = seed.connect_to_prodev()

        if connection:
            seed.create_table(connection)
            seed.insert_data(connection, 'user_data.csv')
            
            # View all data to verify insertion
            seed.view_all_data(connection)
            
            cursor = connection.cursor()
            
            # Check if database exists by querying the table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_data';")
            result = cursor.fetchone()
            if result:
                print(f"Table user_data is present")
            
            cursor.execute("SELECT * FROM user_data LIMIT 5;")
            rows = cursor.fetchall()
            print("\nFirst 5 rows:")
            for row in rows:
                print(row)
            
            cursor.close()
            connection.close()
            print("Database saved as ALX_prodev.db")