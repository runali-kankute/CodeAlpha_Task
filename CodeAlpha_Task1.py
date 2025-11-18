import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound
import tempfile
import pyperclip
import os

# ----------- Window Setup -----------
root = tk.Tk()
root.title("🌐 Language Translation Tool")
root.geometry("700x480")
root.config(bg="#f0f0f0")

# ----------- Title -----------
tk.Label(root, text="Language Translation Tool", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

# ----------- Input Text -----------
tk.Label(root, text="Enter text to translate:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=10)
input_text = tk.Text(root, height=6, width=80, wrap="word")
input_text.pack(padx=10, pady=5)

# ----------- Language Dropdowns -----------
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=10, pady=5)

languages = GoogleTranslator().get_supported_languages()  # list of languages

src_lang = ttk.Combobox(frame, values=languages, width=25)
src_lang.set("english")
src_lang.grid(row=0, column=0, padx=10)

dest_lang = ttk.Combobox(frame, values=languages, width=25)
dest_lang.set("hindi")
dest_lang.grid(row=0, column=1, padx=10)

# ----------- Output Text -----------
tk.Label(root, text="Translated text:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=10)
output_text = tk.Text(root, height=6, width=80, wrap="word")
output_text.pack(padx=10, pady=5)

# ----------- Functions -----------
def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter text!")
        return
    
    try:
        translated = GoogleTranslator(source=src_lang.get(), target=dest_lang.get()).translate(text)
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", translated)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed:\n{e}")

def copy_text():
    text = output_text.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Translated text copied!")
    else:
        messagebox.showwarning("Warning", "No text to copy!")

def speak_text():
    text = output_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "No text to speak!")
        return

    try:
        tts = gTTS(text)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        temp_file.close()

        playsound.playsound(temp_file.name)
        os.remove(temp_file.name)
    except Exception as e:
        messagebox.showerror("Error", f"Speech failed:\n{e}")

# ----------- Buttons -----------
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Translate", command=translate_text, bg="#4CAF50", fg="white", width=15)\
    .grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Copy", command=copy_text, bg="#2196F3", fg="white", width=15)\
    .grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Speak", command=speak_text, bg="#FF9800", fg="white", width=15)\
    .grid(row=0, column=2, padx=10)

# ----------- Run App -----------
root.mainloop()
