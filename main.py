import tkinter as tk
from tkinter import scrolledtext
import requests

# Ollama API URL
OLLAMA_API_URL = "http://localhost:11434/api/chat"
chat_history = [{"role": "system", "content": "You are Grokkie, a dark and witty assistant."}]

# Function to handle chat
def chat_with_grokkie():
    user_text = user_input.get().strip()
    if not user_text:
        return

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {user_text}\n")
    chat_box.config(state=tk.DISABLED)

    chat_history.append({"role": "user", "content": user_text})
    user_input.delete(0, tk.END)

    try:
        payload = {"model": "llama2", "messages": chat_history, "stream": False}
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        bot_reply = response.json()['message']['content'].strip()
    except Exception as e:
        bot_reply = f"GROKKIE: Something went wrong... {e}"

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"GROKKIE: {bot_reply}\n\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

    chat_history.append({"role": "assistant", "content": bot_reply})


# ------ Tkinter UI Setup ------
root = tk.Tk()
root.title("💀 Grokkie!")
root.configure(bg="#121212")
root.geometry("600x500")

# Chat display box
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#1e1e1e", fg="#00FF7F", font=("Consolas", 12))
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_box.config(state=tk.DISABLED)

# User input field
user_input = tk.Entry(root, bg="#2a2a2a", fg="#ffffff", font=("Consolas", 12))
user_input.pack(padx=10, pady=(0, 10), fill=tk.X)
user_input.focus()

# Send button
send_btn = tk.Button(root, text="Send", command=chat_with_grokkie, bg="#333333", fg="#ffffff", font=("Consolas", 12))
send_btn.pack(pady=(0, 15))

# Press Enter to send
user_input.bind("<Return>", lambda event: chat_with_grokkie())

root.mainloop()
