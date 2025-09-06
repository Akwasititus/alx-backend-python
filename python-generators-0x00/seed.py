#!/usr/bin/python3
"""
Database seeding script for ALX_prodev project.
SQLite version - creates database, table, and populates with user data.
"""

import sqlite3
import csv
from io import StringIO
import os


def connect_db():
    """
    Connects to the SQLite database server.
    
    Returns:
        connection: SQLite connection object
    """
    try:
        connection = sqlite3.connect(':memory:')  # In-memory database for testing
        return connection
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return None


def create_database(connection):
    """
    For SQLite, databases are files, so we'll create the database file.
    This function is kept for compatibility with the original interface.
    """
    try:
        # Close the in-memory connection and create a file-based one
        connection.close()
        connection = sqlite3.connect('ALX_prodev.db')
        print("Database ALX_prodev.db created or connected")
        return connection
    except Exception as e:
        print(f"Error creating database: {e}")
        return None


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in SQLite.
    
    Returns:
        connection: SQLite connection object
    """
    try:
        # Check if database file exists, if not create it
        if not os.path.exists('ALX_prodev.db'):
            connection = sqlite3.connect('ALX_prodev.db')
            print("Created new database file: ALX_prodev.db")
        else:
            connection = sqlite3.connect('ALX_prodev.db')
            print("Connected to existing database: ALX_prodev.db")
        return connection
    except Exception as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: SQLite connection object
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """
        cursor.execute(create_table_query)
        
        # Create index
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON user_data (user_id)")
        
        print("Table user_data created successfully")
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error creating table: {e}")


def get_csv_data():
    """
    Returns the CSV data as a string.
    """
    csv_data = """user_id,name,email,age
00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67
006bfede-724d-4cdd-a2a6-59700f40d0da,Glenda Wisozk,Miriam21@gmail.com,119
006e1f7f-90c2-45ad-8c1d-1275d594cc88,Daniel Fahey IV,Delia.Lesch11@hotmail.com,49
00af05c9-0a86-419e-8c2d-5fb7e899ae1c,Ronnie Bechtelar,Sandra19@yahoo.com,22
00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4,Alma Bechtelar,Shelly_Balistreri22@hotmail.com,102
0112b9a4-0c5c-4d14-8d4c-2d9d64b6e6a6,Ms. Della Kshlerin,Elisa.Bergnaum@gmail.com,33
012f3b5c-2d4f-4c6b-9d4c-0d9d64b6e6a6,Mr. John Doe,John.Doe@example.com,25
013e4c6d-3e5g-5h7c-0e5f-1e0e75c7f7b7,Ms. Jane Smith,Jane.Smith@example.com,30
014f5d7e-4f6h-6i8d-1f6g-2f1f86d8g8c8,Dr. Robert Brown,Robert.Brown@example.com,45
015g6e8f-5g7i-7j9e-2g7h-3g2g97e9h9d9,Prof. Emily Davis,Emily.Davis@example.com,50
016h7f9g-6h8j-8k0f-3h8i-4h3h08f0i0e0,Mr. Michael Wilson,Michael.Wilson@example.com,28
017i8g0h-7i9k-9l1g-4i9j-5i4i19g1j1f1,Ms. Sarah Johnson,Sarah.Johnson@example.com,32
018j9h1i-8j0l-0m2h-5j0k-6j5j20h2k2g2,Dr. David Lee,David.Lee@example.com,40
019k0i2j-9k1m-1n3i-6k1l-7k6k31i3l3h3,Prof. Lisa Miller,Lisa.Miller@example.com,38
020l1j3k-0l2n-2o4j-7l2m-8l7l42j4m4i4,Mr. James Taylor,James.Taylor@example.com,29
021m2k4l-1m3o-3p5k-8m3n-9m8m53k5n5j5,Ms. Amanda Harris,Amanda.Harris@example.com,35
022n3l5m-2n4p-4q6l-9n4o-0n9n64l6o6k6,Dr. Christopher Martin,Christopher.Martin@example.com,42
023o4m6n-3o5q-5r7m-0o5p-1o0o75m7p7l7,Prof. Jennifer Anderson,Jennifer.Anderson@example.com,37
024p5n7o-4p6r-6s8n-1p6q-2p1p86n8q8m8,Mr. Thomas Clark,Thomas.Clark@example.com,31
025q6o8p-5q7s-7t9o-2q7r-3q2q97o9r9n9,Ms. Michelle Lewis,Michelle.Lewis@example.com,27
026r7p9q-6r8t-8u0p-3r8s-4r3r08p0s0o0,Dr. Matthew Walker,Matthew.Walker@example.com,44
027s8q0r-7s9u-9v1q-4s9t-5s4s19q1t1p1,Prof. Elizabeth Hall,Elizabeth.Hall@example.com,39
028t9r1s-8t0v-0w2r-5t0u-6t5t20r2u2q2,Mr. Andrew Young,Andrew.Young@example.com,26
029u0s2t-9u1w-1x3s-6u1v-7u6u31s3v3r3,Ms. Stephanie King,Stephanie.King@example.com,34
030v1t3u-0v2x-2y4t-7v2w-8v7v42t4w4s4,Dr. Joshua Wright,Joshua.Wright@example.com,41
031w2u4v-1w3y-3z5u-8w3x-9w8w53u5x5t5,Prof. Nicole Green,Nicole.Green@example.com,36
032x3v5w-2x4z-4a6v-9x4y-0x9x64v6y6u6,Mr. Kevin Adams,Kevin.Adams@example.com,28
033y4w6x-3y5a-5b7w-0y5z-1y0y75w7z7v7,Ms. Heather Baker,Heather.Baker@example.com,33
034z5x7y-4z6b-6c8x-1z6a-2z1z86x8a8w8,Dr. Brian Nelson,Brian.Nelson@example.com,43
035a6y8z-5a7c-7d9y-2a7b-3a2a97y9b9x9,Prof. Samantha Carter,Samantha.Carter@example.com,38
036b7z9a-6b8d-8e0z-3b8c-4b3b08z0c0y0,Mr. Justin Parker,Justin.Parker@example.com,29
037c8a0b-7c9e-9f1a-4c9d-5c4c19a1d1z1,Ms. Rachel Edwards,Rachel.Edwards@example.com,32
038d9b1c-8d0f-0g2b-5d0e-6d5d20b2e2a2,Dr. Timothy Collins,Timothy.Collins@example.com,45
039e0c2d-9e1g-1h3c-6e1f-7e6e31c3f3b3,Prof. Kimberly Stewart,Kimberly.Stewart@example.com,37
040f1d3e-0f2h-2i4d-7f2g-8f7f42d4g4c4,Mr. Jason Turner,Jason.Turner@example.com,30
041g2e4f-1g3i-3j5e-8g3h-9g8g53e5h5d5,Ms. Angela Phillips,Angela.Phillips@example.com,35
042h3f5g-2h4j-4k6f-9h4i-0h9h64f6i6e6,Dr. Jeffrey Campbell,Jeffrey.Campbell@example.com,42
043i4g6h-3i5k-5l7g-0i5j-1i0i75g7j7f7,Prof. Brittany Parker,Brittany.Parker@example.com,39
044j5h7i-4j6l-6m8h-1j6k-2j1j86h8k8g8,Mr. Ryan Evans,Ryan.Evans@example.com,27
045k6i8j-5k7m-7n9i-2k7l-3k2k97i9l9h9,Ms. Hannah Rogers,Hannah.Rogers@example.com,31
046l7j9k-6l8n-8o0j-3l8m-4l3l08j0m0i0,Dr. Paul Barnes,Paul.Barnes@example.com,44
047m8k0l-7m9o-9p1k-4m9n-5m4m19k1n1j1,Prof. Christina Ross,Christina.Ross@example.com,36
048n9l1m-8n0p-0q2l-5n0o-6n5n20l2o2k2,Mr. Scott Howard,Scott.Howard@example.com,26
049o0m2n-9o1q-1r3m-6o1p-7o6o31m3p3l3,Ms. Vanessa Long,Vanessa.Long@example.com,34
050p1n3o-0p2r-2s4n-7p2q-8p7p42n4q4m4,Dr. Gregory James,Gregory.James@example.com,41"""
    return csv_data


def insert_data(connection, data_source):
    """
    Inserts data into the database if it does not exist.
    
    Args:
        connection: SQLite connection object
        data_source: Source of the data
    """
    try:
        cursor = connection.cursor()
        
        # Check if table already has data
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("Data already exists in the table. Skipping insertion.")
            return
        
        # Get CSV data from string
        csv_data = get_csv_data()
        csv_reader = csv.reader(StringIO(csv_data))
        next(csv_reader)  # Skip header row
        
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (?, ?, ?, ?)
        """
        
        batch_data = []
        
        for row in csv_reader:
            if len(row) >= 4:
                user_id = row[0]
                name = row[1]
                email = row[2]
                age = row[3]
                
                batch_data.append((user_id, name, email, age))
        
        # Insert all records
        cursor.executemany(insert_query, batch_data)
        
        connection.commit()
        print(f"Data inserted successfully")
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()


def insert_data(connection, data_source):
    """
    Inserts data into the database if it does not exist.
    """
    try:
        cursor = connection.cursor()
        
        # Check if table already has data
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        print(f"Current record count in user_data: {count}")
        
        if count > 0:
            print("Data already exists in the table. Skipping insertion.")
            return
        
        # Get CSV data from string
        csv_data = get_csv_data()
        csv_reader = csv.reader(StringIO(csv_data))
        next(csv_reader)  # Skip header row
        
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (?, ?, ?, ?)
        """
        
        batch_data = []
        record_count = 0
        
        for row in csv_reader:
            if len(row) >= 4:
                user_id = row[0]
                name = row[1]
                email = row[2]
                age = row[3]
                
                batch_data.append((user_id, name, email, age))
                record_count += 1
        
        # Insert all records
        cursor.executemany(insert_query, batch_data)
        
        connection.commit()
        print(f"Successfully inserted {record_count} records")
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()


def view_all_data(connection):
    """
    View all data in the user_data table
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        rows = cursor.fetchall()
        
        print("\nAll data in user_data table:")
        print("-" * 80)
        for row in rows:
            print(row)
        print("-" * 80)
        print(f"Total records: {len(rows)}")
        
        cursor.close()
    except Exception as e:
        print(f"Error viewing data: {e}")


if __name__ == "__main__":
    # For testing the script directly
    connection = connect_db()
    if connection:
        connection = create_database(connection)
        if connection:
            create_table(connection)
            insert_data(connection, 'internal_data')
            
            # Verify data was inserted
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM user_data")
            count = cursor.fetchone()[0]
            print(f"Inserted {count} records into user_data table")
            
            cursor.execute("SELECT * FROM user_data LIMIT 5")
            rows = cursor.fetchall()
            print("Sample data:")
            for row in rows:
                print(row)
            
            cursor.close()
            connection.close()
            print("Database saved as ALX_prodev.db")
            print("You can open this file with DB Browser for SQLite")