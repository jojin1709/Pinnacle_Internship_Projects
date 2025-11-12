import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyrebase
from datetime import datetime

firebase_config = {
    "apiKey": "",
    "authDomain": "chat-app-project-9b43e.firebaseapp.com",
    "databaseURL": "https://chat-app-project-9b43e-default-rtdb.firebaseio.com/",
    "storageBucket": "chat-app-project-9b43e.appspot.com"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

root = tk.Tk()
root.title("Firebase Chat App")
root.geometry("420x520")
root.configure(bg="#E8F0F2")

name_label = tk.Label(root, text="Enter your name:", font=("Arial", 12), bg="#E8F0F2")
name_label.pack(pady=(10, 5))

name_entry = tk.Entry(root, width=28, font=("Arial", 12))
name_entry.pack(pady=(0, 10))

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=18, state="disabled", font=("Arial", 10))
chat_area.pack(pady=6, padx=8)

msg_frame = tk.Frame(root, bg="#E8F0F2")
msg_frame.pack(fill="x", padx=8, pady=(6, 12))

msg_entry = tk.Entry(msg_frame, width=30, font=("Arial", 12))
msg_entry.pack(side="left", padx=(0, 8))


def send_message():
    name = name_entry.get().strip()
    message = msg_entry.get().strip()
    if not name or not message:
        messagebox.showwarning("Error", "Enter both name and message")
        return

    timestamp = datetime.now().strftime("%H:%M:%S")
    data = {"name": name, "message": message, "time": timestamp}
    try:
        db.child("messages").push(data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send message:\n{e}")
        return

    msg_entry.delete(0, tk.END)
    load_messages()


def load_messages():
    chat_area.config(state="normal")
    chat_area.delete(1.0, tk.END)
    try:
        messages = db.child("messages").get()
    except Exception as e:
        chat_area.insert(tk.END, f"Error reading DB: {e}\n")
        chat_area.config(state="disabled")
        return

    if messages.each():
        for msg in messages.each():
            info = msg.val()
            t = info.get('time', '--:--')
            n = info.get('name', 'unknown')
            m = info.get('message', '')
            chat_area.insert(tk.END, f"[{t}] {n}: {m}\n")

    chat_area.config(state="disabled")
    chat_area.yview_moveto(1.0)


send_btn = tk.Button(msg_frame, text="Send", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), command=send_message)
send_btn.pack(side="left", padx=(0, 6))

refresh_btn = tk.Button(msg_frame, text="Refresh", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), command=load_messages)
refresh_btn.pack(side="left")

def auto_refresh():
    load_messages()
    root.after(3000, auto_refresh)

auto_refresh()
root.mainloop()
