import tkinter as tk
from tkinter import ttk, Canvas, Scrollbar
from PIL import Image, ImageTk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- FAQ Dataset ----------------
faqs = {
    "Hello": "Hello! You can ask anything.",
    "what are your store hours": "We are open from 9 AM to 9 PM every day.",
    "how can i return a product": "You can return any product within 30 days of purchase.",
    "do you offer home delivery": "Yes, we provide free home delivery for orders above ₹500.",
    "what payment methods do you accept": "We accept cash, credit/debit cards, and UPI payments.",
    "where is your store located": "Our store is located at MG Road, Pune."
}

# ---------------- Custom Tokenizer (no NLTK) ----------------
def preprocess(text):
    text = text.lower()
    tokens = re.findall(r'\b[a-zA-Z]+\b', text)
    return " ".join(tokens)

questions = list(faqs.keys())
answers = list(faqs.values())

processed_questions = [preprocess(q) for q in questions]
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(processed_questions)

def get_answer(user_query):
    user_query_processed = preprocess(user_query)
    user_vec = vectorizer.transform([user_query_processed])
    similarities = cosine_similarity(user_vec, faq_vectors)
    index = similarities.argmax()
    score = similarities[0][index]
    
    if score < 0.2:
        return "Sorry, I couldn’t find an answer. Could you rephrase?"
    return answers[index]

# ---------------- UI Setup ----------------
root = tk.Tk()
root.title("FAQ Chatbot")
root.geometry("650x720")
root.config(bg="#f2f3f5")
root.resizable(False, False)

# ---------------- Header ----------------
header = tk.Frame(root, bg="#3b82f6", height=70)
header.pack(fill="x")

title = tk.Label(header, text="FAQ Chatbot", bg="#3b82f6", fg="white",
                 font=("Segoe UI", 20, "bold"))
title.place(x=100, y=18)

# Optional bot icon
try:
    img = Image.open("bot_icon.png").resize((50, 50))
    bot_icon = ImageTk.PhotoImage(img)
    tk.Label(header, image=bot_icon, bg="#3b82f6").place(x=20, y=10)
except:
    pass

# ---------------- Chat Frame ----------------
chat_frame = tk.Frame(root, bg="#ffffff", bd=0)
chat_frame.pack(padx=20, pady=(10, 5), fill="both", expand=True)

canvas = Canvas(chat_frame, bg="#ffffff", highlightthickness=0)
scrollbar = Scrollbar(chat_frame, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#ffffff")
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ---------------- Message Bubbles ----------------
def create_bubble(text, sender="bot"):
    bubble = tk.Frame(
        scrollable_frame,
        bg="#e0e7ff" if sender == "user" else "#f3f4f6",
        padx=12, pady=8
    )
    label = tk.Label(bubble, text=text, bg=bubble["bg"], justify="left",
                     wraplength=400, font=("Segoe UI", 12), fg="#111827")
    label.pack()

    if sender == "user":
        bubble.pack(anchor="e", padx=10, pady=5)
    else:
        bubble.pack(anchor="w", padx=10, pady=5)

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

# ---------------- Input Area ----------------
input_frame = tk.Frame(root, bg="#f2f3f5", height=70)
input_frame.pack(fill="x", padx=20, pady=(0, 15))

entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)

def send_message():
    user_input = entry.get().strip()
    if user_input == "":
        return
    create_bubble(user_input, sender="user")
    entry.delete(0, tk.END)
    bot_reply = get_answer(user_input)
    root.after(500, lambda: create_bubble(bot_reply, sender="bot"))

send_btn = ttk.Button(input_frame, text="Send", command=send_message)
send_btn.pack(side="right", pady=10)

entry.bind("<Return>", lambda e: send_message())

# ---------------- Initial Bot Message ----------------
create_bubble("Hello! I’m your FAQ assistant. Ask me anything about our store.", "bot")

root.mainloop()

