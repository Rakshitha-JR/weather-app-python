import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
print("new UI running")

API_KEY = "af2d081b776a33c94b9bbcf5dae4afcd"

def get_weather():
    city = city_entry.get().strip().title()

    if city == "":
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            temp = round(data["main"]["temp"], 1)
            feels_like = round(data["main"]["feels_like"], 1)
            humidity = data["main"]["humidity"]
            weather = data["weather"][0]["description"]
            wind = data["wind"]["speed"]

            # 🌤️ Get icon
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_response.content))
            icon_photo = ImageTk.PhotoImage(icon_image)

            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo

            result = (
                f"{city}\n"
                f"🌡️ Temp: {temp}°C\n"
                f"🤒 Feels: {feels_like}°C\n"
                f"🌥️ {weather}\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬️ Wind: {wind} m/s"
            )

            result_label.config(text=result)

        else:
            messagebox.showerror("Error", "❌ City not found")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# 🎨 UI Window
root = tk.Tk()
root.title("Weather App 🌦️")
root.geometry("350x420")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

# Title
tk.Label(root, text="Weather App 🌦️", font=("Arial", 18, "bold"),
         bg="#1e1e2f", fg="white").pack(pady=10)

# Input
city_entry = tk.Entry(root, font=("Arial", 14), justify="center")
city_entry.pack(pady=10)

# Button
tk.Button(root, text="Get Weather", command=get_weather,
          bg="#4CAF50", fg="white", font=("Arial", 12), width=15).pack(pady=10)

# Icon
icon_label = tk.Label(root, bg="#1e1e2f")
icon_label.pack()

# Result
result_label = tk.Label(root, text="", font=("Arial", 12),
                        bg="#1e1e2f", fg="white", justify="center")
result_label.pack(pady=10)

# Run app
root.mainloop()