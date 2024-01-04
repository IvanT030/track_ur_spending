import sqlite3
import keyboard
import response

conn = sqlite3.connect('track_your_spending.db')

#c = conn.cursor()
#c.execute("""CREATE TABLE spending(
#    year integer,
#    month integer,
#    day integer,         
#    category text,
#    cost integer
#)""")

conn.commit()

conn.close()