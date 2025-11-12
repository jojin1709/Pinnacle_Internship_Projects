import tkinter as tk
from tkinter import messagebox
import datetime
import time
import threading
from playsound import playsound

# ----- Functions -----
def set_alarm():
    alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
    if alarm_time == "::":
        messagebox.showwarning("Input Error", "Please set a valid time!")
    else:
        messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")
        threading.Thread(target=alarm_thread, args=(alarm_time,), daemon=True).start()

def alarm_thread(set_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == set_time:
            messagebox.showinfo("Alarm", "Wake up! It's time!")
            try:
                playsound("alarm_sound.mp3")  # keep an mp3 file in same folder
            except:
                messagebox.showerror("Error", "Alarm sound file not found!")
            break
        time.sleep(1)

# ----- GUI -----
root = tk.Tk()
root.title("Alarm Clock - Pinnacle Labs")
root.geometry("360x250")
root.resizable(False, False)

tk.Label(root, text="Set Time (24-hour format)", font=("Arial", 14, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

hour = tk.StringVar()
minute = tk.StringVar()
second = tk.StringVar()

tk.Entry(frame, textvariable=hour, width=5, font=("Arial", 18)).grid(row=0, column=0, padx=5)
tk.Label(frame, text=":", font=("Arial", 18)).grid(row=0, column=1)
tk.Entry(frame, textvariable=minute, width=5, font=("Arial", 18)).grid(row=0, column=2, padx=5)
tk.Label(frame, text=":", font=("Arial", 18)).grid(row=0, column=3)
tk.Entry(frame, textvariable=second, width=5, font=("Arial", 18)).grid(row=0, column=4, padx=5)

tk.Button(root, text="Set Alarm", font=("Arial", 14), bg="#4CAF50", fg="white", command=set_alarm).pack(pady=20)

root.mainloop()
