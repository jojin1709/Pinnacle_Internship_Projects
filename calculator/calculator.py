import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("Basic Calculator - Pinnacle Labs")
root.geometry("350x480")
root.resizable(False, False)

# Entry widget
expression = ""
input_text = tk.StringVar()

def press(num):
    global expression
    expression += str(num)
    input_text.set(expression)

def clear():
    global expression
    expression = ""
    input_text.set("")

def equalpress():
    try:
        global expression
        total = str(eval(expression))
        input_text.set(total)
        expression = total
    except:
        messagebox.showerror("Error", "Invalid Expression")
        expression = ""
        input_text.set("")

# Entry display
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)
entry = tk.Entry(entry_frame, font=('Arial', 20, 'bold'),
                 textvariable=input_text, width=18, borderwidth=5, relief="ridge", justify='right')
entry.grid(row=0, column=0)
entry.pack()

# Button layout
btn_frame = tk.Frame(root)
btn_frame.pack()

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', 'C', '+']
]

for i in range(4):
    for j in range(4):
        b = tk.Button(btn_frame, text=buttons[i][j], width=7, height=3,
                      font=('Arial', 14), command=lambda x=buttons[i][j]: press(x) if x not in ['C'] else clear())
        b.grid(row=i, column=j, padx=3, pady=3)

equal_button = tk.Button(root, text='=', width=32, height=3, font=('Arial', 14), bg='#4CAF50', fg='white', command=equalpress)
equal_button.pack(pady=5)

root.mainloop()
