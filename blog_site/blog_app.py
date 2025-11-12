import tkinter as tk
from tkinter import messagebox, scrolledtext
import json, os

DATA_FILE = "blogs.json"

# ---------------------- Data Handling ----------------------
def load_blogs():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_blogs(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------------- Functions ----------------------
def refresh_listbox():
    listbox.delete(0, tk.END)
    for post in blogs:
        listbox.insert(tk.END, post["title"])

def new_post():
    title = title_entry.get().strip()
    content = text_area.get("1.0", tk.END).strip()
    if not title or not content:
        messagebox.showwarning("Missing Data", "Please enter both title and content.")
        return
    blogs.append({"title": title, "content": content})
    save_blogs(blogs)
    refresh_listbox()
    title_entry.delete(0, tk.END)
    text_area.delete("1.0", tk.END)
    messagebox.showinfo("Saved", "New blog post added successfully!")

def view_post():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select Post", "Please select a post to view.")
        return
    index = sel[0]
    post = blogs[index]
    title_entry.delete(0, tk.END)
    title_entry.insert(0, post["title"])
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, post["content"])

def update_post():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select Post", "Please select a post to update.")
        return
    index = sel[0]
    blogs[index]["title"] = title_entry.get().strip()
    blogs[index]["content"] = text_area.get("1.0", tk.END).strip()
    save_blogs(blogs)
    refresh_listbox()
    messagebox.showinfo("Updated", "Blog post updated successfully!")

def delete_post():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select Post", "Please select a post to delete.")
        return
    index = sel[0]
    if messagebox.askyesno("Delete", f"Delete '{blogs[index]['title']}'?"):
        blogs.pop(index)
        save_blogs(blogs)
        refresh_listbox()
        title_entry.delete(0, tk.END)
        text_area.delete("1.0", tk.END)
        messagebox.showinfo("Deleted", "Post deleted successfully.")

# ---------------------- UI Setup ----------------------
root = tk.Tk()
root.title("📰 Blog Platform - Dark Mode")
root.geometry("850x500")
root.config(bg="#1e1e1e")

blogs = load_blogs()

# Left Panel (List of Posts)
left_frame = tk.Frame(root, bg="#1e1e1e")
left_frame.pack(side="left", fill="y", padx=10, pady=10)

tk.Label(left_frame, text="Your Posts", bg="#1e1e1e", fg="#00FF88",
         font=("Arial", 12, "bold")).pack(pady=5)
listbox = tk.Listbox(left_frame, width=30, height=25, bg="#252526",
                     fg="white", selectbackground="#007ACC", font=("Arial", 10))
listbox.pack(padx=5, pady=5)

# Buttons
tk.Button(left_frame, text="View", bg="#007ACC", fg="white",
          command=view_post, width=10).pack(pady=3)
tk.Button(left_frame, text="Delete", bg="#E53935", fg="white",
          command=delete_post, width=10).pack(pady=3)

# Right Panel (Editor)
right_frame = tk.Frame(root, bg="#1e1e1e")
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(right_frame, text="Title", bg="#1e1e1e", fg="#00FF88",
         font=("Arial", 11, "bold")).pack(anchor="w")
title_entry = tk.Entry(right_frame, width=50, font=("Arial", 12),
                       bg="#333333", fg="white", insertbackground="white")
title_entry.pack(fill="x", pady=5)

tk.Label(right_frame, text="Content", bg="#1e1e1e", fg="#00FF88",
         font=("Arial", 11, "bold")).pack(anchor="w")
text_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD,
                                      width=70, height=15, font=("Arial", 11),
                                      bg="#252526", fg="white", insertbackground="white")
text_area.pack(pady=5)

# Action Buttons
btn_frame = tk.Frame(right_frame, bg="#1e1e1e")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="New Post", bg="#4CAF50", fg="white",
          width=12, command=new_post).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", bg="#FFC107", fg="black",
          width=12, command=update_post).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Clear", bg="#9E9E9E", fg="black",
          width=12, command=lambda: [title_entry.delete(0, tk.END),
                                     text_area.delete("1.0", tk.END)]).grid(row=0, column=2, padx=5)

refresh_listbox()

root.mainloop()
