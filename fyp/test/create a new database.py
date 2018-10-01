import sqlite3


with sqlite3.connect("Quiz.db")as db:
    cursor=db.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS USER(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
firstname VARCHAR(20) NOT NULL,
surname VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL);
''')

cursor.execute("""
INSERT INTO USER(username,firstname,surname,password)
VALUES("admin1","admin","one","admin")
""")
db.commit()

cursor.execute("SELECT * FROM USER")
print(cursor.fetchall())