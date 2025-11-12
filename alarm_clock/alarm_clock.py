import tkinter as tk
from tkinter import messagebox
import datetime
import time
import threading
import winsound  # built-in for Windows sound

# ----- Alarm Logic -----
def set_alarm():
    alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
    if alarm_time == "::":
        messagebox.showwarning("Input Error", "Please set a valid time!")
        return

    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")
    threading.Thread(target=alarm_thread, args=(alarm_time,), daemon=True).start()


def alarm_thread(set_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == set_time:
            messagebox.showinfo("Alarm", "Wake up! It's time!")
            try:
                for _ in range(5):
                    winsound.Beep(1000, 600)  # frequency (Hz), duration (ms)
                    time.sleep(0.5)
                root.destroy()  # close window after ringing
            except Exception as e:
                messagebox.showerror("Error", f"Sound failed: {e}")
            break
        time.sleep(1)


# ----- Live Clock Display -----
def update_clock():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=f"Current Time: {current_time}")
    clock_label.after(1000, update_clock)  # update every second


# ----- GUI -----
root = tk.Tk()
root.title("Alarm Clock - Pinnacle Labs")
root.geometry("380x280")
root.resizable(False, False)

# Heading
tk.Label(root, text="Set Time (24-hour format)", font=("Arial", 14, "bold")).pack(pady=10)

# Live Clock
clock_label = tk.Label(root, text="", font=("Arial", 12))
clock_label.pack()
update_clock()

# Input Fields
frame = tk.Frame(root)
frame.pack(pady=10)

hour = tk.StringVar()
minute = tk.StringVar()
second = tk.StringVar()

tk.Entry(frame, textvariable=hour, width=5, font=("Arial", 18)).grid(row=0, column=0, padx=5)
tk.Label(frame, text=":", font=("Arial", 18)).grid(row=0, column=1)
tk.Entry(frame, textvariable=minute, width=5, font=("Arial", 18)).grid(row=0, column=2, padx=5)
tk.Label(frame, text=":", font=("Arial", 18)).grid(row=0, column=3)
tk.Entry(frame, textvariable=second, width=5, font=("Arial", 18)).grid(row=0, column=4, padx=5)

# Set Alarm Button
tk.Button(root, text="Set Alarm", font=("Arial", 14), bg="#4CAF50", fg="white",
          command=set_alarm).pack(pady=20)

# Footer Label
tk.Label(root, text="Developed for Pinnacle Labs Internship 2025",
         font=("Arial", 9), fg="gray").pack(side="bottom", pady=10)

root.mainloop()
