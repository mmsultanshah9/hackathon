import pyodbc

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-3V4IM9T;'
    'DATABASE=hackathon;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()
cursor.execute("SELECT name FROM sys.tables")

for row in cursor.fetchall():
    print(row)

conn.close()
