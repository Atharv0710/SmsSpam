import sqlite3

conn = sqlite3.connect('spam_logs.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS logs
             (message TEXT, prediction TEXT)''')
conn.commit()
conn.close()
