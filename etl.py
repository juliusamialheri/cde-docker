import psycopg2
import pandas as pd
import time

# Database connection parameters
DB_HOST = 'db'  # This is the name of the DB container on the shared network
DB_NAME = 'mydb'
DB_USER = 'user'
DB_PASS = 'pass'

def wait_for_db():
    """Wait for the database to become available."""
    for _ in range(30):  # Try for 30 seconds
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            conn.close()
            print("Database is ready.")
            return
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(1)
    raise Exception("Database not available after waiting.")

def create_table(cur):
    """Create the target table if it doesn't exist."""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            age INTEGER
        );
    """)

def extraction():
    """Extraction: Generate dummy data."""
    data = [
        {'name': 'alice', 'age': 25},
        {'name': 'bob', 'age': 17},
        {'name': 'charlie', 'age': 30},
        {'name': 'dave', 'age': 16},
        {'name': 'eve', 'age': 28}
    ]
    print("Extracted data:", data)
    return data

def transformation(data):
    """Transformation: Filter adults and uppercase names using pandas."""
    df = pd.DataFrame(data)
    df = df[df['age'] >= 18]  # Filter adults
    df['name'] = df['name'].str.upper()  # Uppercase names
    transformed_data = df.to_dict(orient='records')
    print("Transformed data:", transformed_data)
    return transformed_data

def loading(transformed_data):
    """Loading: Insert data into the database."""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    
    create_table(cur)
    
    for row in transformed_data:
        cur.execute("""
            INSERT INTO users (name, age) VALUES (%s, %s);
        """, (row['name'], row['age']))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded into database.")

if __name__ == "__main__":
    wait_for_db()
    extracted = extraction()
    transformed = transformation(extracted)
    loading(transformed)
    print("ETL pipeline completed.")