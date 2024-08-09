import tkinter as tk
from tkinter import PhotoImage, Text, END, Label, Button, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from urllib.parse import urlparse, parse_qs
import subprocess
import re

def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def get_video_id(url):
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
        if video_id is None:
            messagebox.showerror("Hata", "Geçersiz YouTube URL'si.")
            return None
        return video_id
    except Exception as e:
        messagebox.showerror("Hata", f"Video ID alınırken hata oluştu: {str(e)}")
        return None

def get_thumbnail_url(video_id):
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

def show_thumbnail(url):
    try:
        print(f"Video Resim URL'si: {url}")  # URL'yi kontrol etmek için print
        response = requests.get(url)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        thumbnail_label.config(image=img_tk)
        thumbnail_label.image = img_tk
    except requests.exceptions.RequestException as req_err:
        print(f"HTTP Hatası: {str(req_err)}")  # Hata mesajını kontrol
        messagebox.showerror("Hata", f"HTTP Hatası: {str(req_err)}")
    except Exception as e:
        print(f"Küçük resim yüklenirken bir hata oluştu: {str(e)}")
        messagebox.showerror("Hata", f"Küçük resim yüklenirken bir hata oluştu: {str(e)}")

def run_test():
    input_url = input_text_area.get("1.0", "end-1c")  # Metin giriş alanından URL'yi al
    if not input_url.strip():
        messagebox.showwarning("Uyarı", "Lütfen test edilecek bir YouTube URL'si girin.")
        return

    video_id = get_video_id(input_url)
    if video_id is None:
        return

    thumbnail_url = get_thumbnail_url(video_id)
    show_thumbnail(thumbnail_url)

    try:
        result = subprocess.run(["python", "modelTT.py", input_url], capture_output=True, text=True)
        clean_output = remove_ansi_escape_sequences(result.stdout)
        clean_output = clean_output.strip().lower()
        output_text_area.delete("1.0", END)
        output_text_area.insert(END, clean_output)
    except Exception as e:
        messagebox.showerror("Hata", f"Test sırasında bir hata oluştu: {str(e)}")

# Ana pencereyi oluştur
root = tk.Tk()
root.title("İçerik Muhafızı")
root.geometry("1200x800")
root.configure(bg="#2c3e50")

try:
    logo = PhotoImage(file="logo.png")
    logo = logo.subsample(3, 3)
    logo_label = Label(root, image=logo, bg="#2c3e50")
    logo_label.pack(pady=3) #10
except Exception as e:
    messagebox.showerror("Hata", f"Logo yüklenirken bir hata oluştu: {str(e)}")

title_label = Label(root, text="İçerik Muhafızı", font=("Arial", 24, "bold"), fg="#00bf63", bg="#2c3e50")
title_label.pack(pady=0)

input_text_area = Text(root, height=5, width=80, bg="#2c3e50", font=("Arial", 12), fg="white")
input_text_area.pack(padx=10, pady=7)
input_text_area.insert("1.0", "Test edilecek YouTube video URL'sini buraya girin...")

def clear_text(event):
    current_text = input_text_area.get("1.0", "end-1c")
    if current_text == "Test edilecek YouTube video URL'sini buraya girin...":
        input_text_area.delete("1.0", END)
        input_text_area.unbind("<Button-1>")

input_text_area.bind("<Button-1>", clear_text)

test_button = Button(root, text="İçerik Testi Yap", command=run_test, font=("Arial", 14), fg="#ecf0f1", bg="#2c3e50")
test_button.pack(pady=20)
test_button.config(bg="#2c3e50", activebackground="#00bf63")

output_text_area = Text(root, height=5, width=80, state="normal", bg="#2c3e50", font=("Arial", 12), fg="#00bf63")
output_text_area.pack(padx=10, pady=10)

thumbnail_label = Label(root, bg="#2c3e50")
thumbnail_label.pack(pady=20)

root.mainloop()
