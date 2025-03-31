import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create food_items table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL
    )
''')

# Insert sample food items
cursor.executemany('''
    INSERT INTO food_items (name, price, category) VALUES (?, ?, ?)
''', [
    ("Veg Burger", 50, "Fast Food"),
    ("Chicken Biryani", 150, "Main Course"),
    ("Paneer Butter Masala", 120, "Main Course"),
    ("Coca Cola", 30, "Beverage")
])

conn.commit()
conn.close()

print("Database setup complete! Food items added.")
