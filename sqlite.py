import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME VARCHAR(25),
        CLASS VARCHAR(25),
        SECTION VARCHAR(25),
        MARKS INTEGER
    )
""")

cursor.executemany(
    "INSERT INTO STUDENT VALUES (?, ?, ?, ?)",
    [
        ("Arjun Kumar", "10", "A", 85),
        ("Priya Sharma", "10", "B", 92),
        ("Rahul Verma", "9", "A", 78),
        ("Sneha Patel", "9", "B", 88),
        ("Vikram Singh", "10", "A", 95),
        ("Ananya Gupta", "9", "A", 72),
        ("Rohan Mehta", "10", "B", 68),
        ("Divya Nair", "9", "B", 91),
        ("Karan Joshi", "10", "A", 83),
        ("Meera Reddy", "9", "A", 76),
    ]
)

conn.commit()
conn.close()
print("student.db created successfully!")