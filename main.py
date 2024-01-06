###################################
#c.execute('''CREATE TABLE spending
#       (Year INT NOT NULL,
#        Month INT NOT NULL,
#        Day INT NOT NULL,
#        Spending_Category TEXT,
#        Expense_Item TEXT,
#        Cost INT);''')
###################################
import sqlite3
import asyncio
from response import main
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('track_your_spending.db')
c = conn.cursor()
#or text in result:
#    c.execute(f"""INSERT INTO spending 
#        (Year,Month,Day,Spending_Category,Expense_Item,Cost)
#        VALUES ({text[2]}, {text[3]}, {text[4]}, '{text[1]}', '{text[0]}', {text[5]})""")
recording = 0 #0 = startRecord, 1 = stoprecord     

# Function to handle clicking on the microphone button.
def on_microphone_click():
    if recording == 0:
        result = asyncio.run(main())
        result_text.set("Processing complete. Press OK to continue or Cancel to re-record.")

# Function to handle the OK button click.
def on_ok_click():
    # Here you would handle saving to the database and resetting the UI.
    # Reset the result_text widget to initial state.
    result_text.set("Please click the microphone to start recording.")

# Function to handle the Cancel button click.
def on_cancel_click():
    # Here you would reset the recording process and UI.
    result_text.set("Recording canceled. Please click the microphone to start recording.")

root = tk.Tk()
root.title("Voice-Controlled Accounting System")

# Result text variable
result_text = tk.StringVar()
result_text.set("Please click the microphone to start recording.")

# Microphone button
microphone_button = tk.Button(root, text="🎤", command=on_microphone_click)
microphone_button.pack()

# Result display
result_label = tk.Label(root, textvariable=result_text)
result_label.pack()

# OK button
ok_button = tk.Button(root, text="OK", command=on_ok_click)
ok_button.pack(side=tk.LEFT)

# Cancel button
cancel_button = tk.Button(root, text="Cancel", command=on_cancel_click)
cancel_button.pack(side=tk.RIGHT)

# Run the application
root.mainloop()

conn.commit()
conn.close()