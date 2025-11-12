import tkinter as tk
from tkinter import messagebox

questions = [
    {
        "q": "What is the capital of India?",
        "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
        "answer": "Delhi"
    },
    {
        "q": "Which programming language is used for web apps?",
        "options": ["Python", "C", "C++", "Java"],
        "answer": "Python"
    },
    {
        "q": "What is 7 * 8?",
        "options": ["54", "56", "64", "48"],
        "answer": "56"
    },
    {
        "q": "Which company developed Windows?",
        "options": ["Apple", "Microsoft", "Google", "IBM"],
        "answer": "Microsoft"
    },
    {
        "q": "What does GUI stand for?",
        "options": ["Graphical User Interface", "Global User Interaction", "Graphical Utility Input", "General UI"],
        "answer": "Graphical User Interface"
    }
]

score = 0
index = 0

def check_answer(selected):
    global score, index
    if selected == questions[index]["answer"]:
        score += 1
    index += 1
    if index < len(questions):
        show_question()
    else:
        messagebox.showinfo("Quiz Completed", f"Your Score: {score}/{len(questions)}")
        root.destroy()

def show_question():
    q_label.config(text=questions[index]["q"])
    for i in range(4):
        btns[i].config(text=questions[index]["options"][i], command=lambda x=questions[index]["options"][i]: check_answer(x))

root = tk.Tk()
root.title("Quiz App")
root.geometry("500x350")
root.resizable(False, False)
root.configure(bg="#F4F6F7")

q_label = tk.Label(root, text="", font=("Arial", 14, "bold"), wraplength=400, bg="#F4F6F7")
q_label.pack(pady=20)

btns = []
for i in range(4):
    b = tk.Button(root, text="", font=("Arial", 12), width=25, bg="#4CAF50", fg="white")
    b.pack(pady=5)
    btns.append(b)

show_question()
root.mainloop()
