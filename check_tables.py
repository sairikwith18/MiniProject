import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Function to print table contents
def print_table(table_name):
    print(f"\nContents of {table_name} table:")
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)

# Get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:", tables)

# Print contents of each table
for table in tables:
    table_name = table[0]
    if table_name != "sqlite_sequence":  # Ignore SQLite internal table
        print_table(table_name)

conn.close()
