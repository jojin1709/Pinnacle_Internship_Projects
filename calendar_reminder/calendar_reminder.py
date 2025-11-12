import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
import datetime
import json
import os
import threading
import time

DATA_FILE = "reminders.json"

# ---------- Data Handling ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def ensure_path(data, y, m, d):
    ys, ms, ds = str(y), str(m), str(d)
    if ys not in data: data[ys] = {}
    if ms not in data[ys]: data[ys][ms] = {}
    if ds not in data[ys][ms]: data[ys][ms][ds] = []
    return data

def add_reminder(y, m, d, time_str, text):
    data = load_data()
    ensure_path(data, y, m, d)
    data[str(y)][str(m)][str(d)].append({"time": time_str, "text": text, "done": False})
    save_data(data)

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Calendar Reminder - Dark Mode")
root.geometry("760x540")
root.configure(bg="#1e1e1e")

sel_year = tk.IntVar(value=datetime.date.today().year)
sel_month = tk.IntVar(value=datetime.date.today().month)
sel_day = tk.IntVar(value=datetime.date.today().day)

# ---------- Functions ----------
def update_listbox_for_selected():
    lb_reminders.delete(0, tk.END)
    y, m, d = str(sel_year.get()), str(sel_month.get()), str(sel_day.get())
    arr = data_store.get(y, {}).get(m, {}).get(d, [])
    for r in arr:
        lb_reminders.insert(tk.END, f"{r['time']}  —  {r['text']}")

def on_select_day(day):
    sel_day.set(day)
    lbl_selected_day.config(
        text=f"Selected: {sel_year.get()}-{sel_month.get():02d}-{sel_day.get():02d}"
    )
    update_listbox_for_selected()

def build_calendar():
    for w in cal_frame.winfo_children():
        w.destroy()
    y, m = sel_year.get(), sel_month.get()
    cal = calendar.monthcalendar(y, m)
    lbl_month.config(text=f"{calendar.month_name[m]} {y}")

    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    for ci, d in enumerate(days):
        tk.Label(cal_frame, text=d, font=("Arial", 10, "bold"), fg="white", bg="#1e1e1e").grid(row=0, column=ci)

    for r, week in enumerate(cal, start=1):
        for c, day in enumerate(week):
            if day == 0:
                tk.Label(cal_frame, text="", width=5, height=2, bg="#1e1e1e").grid(row=r, column=c)
            else:
                btn = tk.Button(
                    cal_frame, text=str(day), width=5, height=2, bg="#333333", fg="white",
                    activebackground="#4CAF50",
                    command=lambda day=day: on_select_day(day)
                )
                today = datetime.date.today()
                if y == today.year and m == today.month and day == today.day:
                    btn.configure(bg="#444444", fg="#00FF88")
                btn.grid(row=r, column=c, padx=2, pady=2)

def on_prev_month():
    m, y = sel_month.get() - 1, sel_year.get()
    if m < 1: m, y = 12, y - 1
    sel_month.set(m); sel_year.set(y); build_calendar()

def on_next_month():
    m, y = sel_month.get() + 1, sel_year.get()
    if m > 12: m, y = 1, y + 1
    sel_month.set(m); sel_year.set(y); build_calendar()

def add_button_action():
    text = entry_text.get().strip()
    if not text:
        messagebox.showwarning("Empty", "Enter reminder text first")
        return
    time_str = simpledialog.askstring("Time", "Enter time (HH:MM, 24-hour):", parent=root)
    if not time_str: return
    try:
        h, m = map(int, time_str.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60): raise ValueError
    except:
        messagebox.showerror("Invalid", "Time must be in HH:MM format")
        return
    y, mo, d = sel_year.get(), sel_month.get(), sel_day.get()
    add_reminder(y, mo, d, f"{h:02d}:{m:02d}", text)
    global data_store
    data_store = load_data()
    update_listbox_for_selected()
    entry_text.delete(0, tk.END)
    try:
        import winsound; winsound.Beep(800, 150)
    except: pass
    messagebox.showinfo("Success", f"Reminder set for {y}-{mo:02d}-{d:02d} at {h:02d}:{m:02d}")

def del_button_action():
    sel = lb_reminders.curselection()
    if not sel:
        messagebox.showinfo("Select", "Select a reminder to delete")
        return
    idx = sel[0]
    y, mo, d = sel_year.get(), sel_month.get(), sel_day.get()
    data = load_data()
    try:
        data[str(y)][str(mo)][str(d)].pop(idx)
        save_data(data)
        global data_store
        data_store = load_data()
        update_listbox_for_selected()
        messagebox.showinfo("Deleted", "Reminder deleted successfully.")
    except: pass

def background_checker():
    while True:
        try:
            now = datetime.datetime.now()
            y, m, d = str(now.year), str(now.month), str(now.day)
            data = load_data()
            reminders = data.get(y, {}).get(m, {}).get(d, [])
            for r in reminders:
                if r.get("done"): continue
                hh, mm = map(int, r["time"].split(":"))
                if hh == now.hour and mm == now.minute:
                    msg = r["text"]
                    try:
                        import winsound
                        winsound.Beep(1200, 200)
                        winsound.Beep(1000, 200)
                    except: pass
                    def popup():
                        messagebox.showinfo("Reminder", f"⏰ {msg}")
                    root.after(0, popup)
                    r["done"] = True
                    save_data(data)
            time.sleep(20)
        except:
            time.sleep(5)

# ---------- UI Layout ----------
top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(pady=6)
tk.Button(top_frame, text="<", width=3, command=on_prev_month, bg="#333", fg="white").grid(row=0, column=0)
lbl_month = tk.Label(top_frame, text="", font=("Arial", 14, "bold"), fg="#00FF88", bg="#1e1e1e")
lbl_month.grid(row=0, column=1, padx=8)
tk.Button(top_frame, text=">", width=3, command=on_next_month, bg="#333", fg="white").grid(row=0, column=2)

cal_frame = tk.Frame(root, bg="#1e1e1e")
cal_frame.pack(pady=8)

right_frame = tk.Frame(root, bg="#1e1e1e")
right_frame.pack(side="right", fill="y", padx=10, pady=6)

lbl_selected_day = tk.Label(right_frame, text="", fg="white", bg="#1e1e1e", font=("Arial", 10))
lbl_selected_day.pack(pady=4)

lb_reminders = tk.Listbox(right_frame, width=40, height=16, bg="#252526", fg="white", selectbackground="#007ACC")
lb_reminders.pack(pady=6)

btn_frame = tk.Frame(right_frame, bg="#1e1e1e")
btn_frame.pack(pady=6)
tk.Button(btn_frame, text="Delete Reminder", width=16, command=del_button_action, bg="#E53935", fg="white").pack(pady=4)

left_bottom = tk.Frame(root, bg="#1e1e1e")
left_bottom.pack(side="left", padx=10, pady=10, fill="both", expand=True)
entry_text = tk.Entry(left_bottom, width=36, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
entry_text.pack(pady=6)
tk.Button(left_bottom, text="Add Reminder", width=16, command=add_button_action, bg="#007ACC", fg="white").pack(pady=4)
tk.Label(left_bottom, text="Type reminder then click Add", fg="#BBBBBB", bg="#1e1e1e").pack()

# ---------- Run ----------
data_store = load_data()
build_calendar()
on_select_day(sel_day.get())
threading.Thread(target=background_checker, daemon=True).start()
root.mainloop()
