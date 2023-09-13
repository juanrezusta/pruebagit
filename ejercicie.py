import sqlite3

conn=sqlite3.connect("database.db")
c=conn.cursor()
query=c.execute("SELECT * FROM products")
queryfetch=query.fetchall()

for i in queryfetch:
    print(i)

