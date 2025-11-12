import tkinter as tk
from tkinter import messagebox
import random

data = {
    "mumbai": {"temp": 31, "humidity": 70, "desc": "Scattered clouds"},
    "kochi": {"temp": 29, "humidity": 82, "desc": "Light rain"},
    "delhi": {"temp": 27, "humidity": 55, "desc": "Clear sky"},
    "chennai": {"temp": 33, "humidity": 68, "desc": "Sunny"},
    "bengaluru": {"temp": 25, "humidity": 60, "desc": "Partly cloudy"},
    "pune": {"temp": 28, "humidity": 66, "desc": "Hazy"},
    "kolkata": {"temp": 30, "humidity": 77, "desc": "Thunderstorms"},
    "hyderabad": {"temp": 32, "humidity": 65, "desc": "Few clouds"}
}

def show_weather():
    city = entry.get().strip().lower()
    if not city:
        messagebox.showwarning("Error", "Enter a city name")
        return
    info = data.get(city, {
        "temp": random.randint(20, 35),
        "humidity": random.randint(40, 85),
        "desc": random.choice(["Clear sky", "Rain", "Cloudy", "Sunny", "Haze"])
    })
    result.config(
        text=f"{city.title()}\nTemp: {info['temp']}°C\nHumidity: {info['humidity']}%\n{info['desc']}"
    )

root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#E8F0F2")

tk.Label(root, text="Weather App", font=("Arial", 16, "bold"), bg="#E8F0F2").pack(pady=10)

frame = tk.Frame(root, bg="#E8F0F2")
frame.pack(pady=10)

tk.Label(frame, text="City:", font=("Arial", 12), bg="#E8F0F2").grid(row=0, column=0, padx=5)
entry = tk.Entry(frame, width=20, font=("Arial", 12))
entry.grid(row=0, column=1, padx=5)

tk.Button(root, text="Check", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=show_weather).pack(pady=10)

result = tk.Label(root, text="", font=("Arial", 13), bg="#E8F0F2", justify="center")
result.pack(pady=20)

root.mainloop()
