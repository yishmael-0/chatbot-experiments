import threading
import tkinter as tk
from tkinter import scrolledtext

from eliza import get_eliza_response
from LLM import get_llm_response


class ChatComparisonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Past vs Present AI - ELIZA vs LLM")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0f172a")

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="AI Comparison Lab: ELIZA vs LLM",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#0f172a"
        )
        title.pack(pady=(15, 5))

        subtitle = tk.Label(
            self.root,
            text="Compare rule-based AI and modern generative AI side by side",
            font=("Segoe UI", 11),
            fg="#cbd5e1",
            bg="#0f172a"
        )
        subtitle.pack(pady=(0, 15))

        top_frame = tk.Frame(self.root, bg="#0f172a")
        top_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.eliza_frame = tk.Frame(top_frame, bg="#1e293b", bd=0, highlightthickness=0)
        self.eliza_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.llm_frame = tk.Frame(top_frame, bg="#1e293b", bd=0, highlightthickness=0)
        self.llm_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        eliza_label = tk.Label(
            self.eliza_frame,
            text="ELIZA (Past AI)",
            font=("Segoe UI", 16, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        eliza_label.pack(pady=10)

        self.eliza_chat = scrolledtext.ScrolledText(
            self.eliza_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#0b1220",
            fg="#e2e8f0",
            insertbackground="white",
            relief="flat",
            padx=10,
            pady=10
        )
        self.eliza_chat.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.eliza_chat.insert(tk.END, "ELIZA ready.\n\n")
        self.eliza_chat.config(state="disabled")

        llm_label = tk.Label(
            self.llm_frame,
            text="LLM (Present AI)",
            font=("Segoe UI", 16, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        llm_label.pack(pady=10)

        self.llm_chat = scrolledtext.ScrolledText(
            self.llm_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#0b1220",
            fg="#e2e8f0",
            insertbackground="white",
            relief="flat",
            padx=10,
            pady=10
        )
        self.llm_chat.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.llm_chat.insert(tk.END, "LLM ready.\n\n")
        self.llm_chat.config(state="disabled")

        bottom_frame = tk.Frame(self.root, bg="#0f172a")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))


        input_label = tk.Label(
            bottom_frame,
            text="Type your message here:",
            font=("Segoe UI", 10),
            fg="#cbd5e1",
            bg="#0f172a",
        )
        input_label.pack(anchor="w", pady=(0, 5))

        self.input_box = tk.Entry(
            bottom_frame,
            font=("Segoe UI", 13),
            bg="#1e293b",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.input_box.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.input_box.bind("<Return>", self.send_message)

        send_btn = tk.Button(
            bottom_frame,
            text="Compare",
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.send_message
        )
        send_btn.pack(side="left", padx=(0, 10))

        clear_btn = tk.Button(
            bottom_frame,
            text="Clear",
            font=("Segoe UI", 12, "bold"),
            bg="#475569",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.clear_chats
        )
        clear_btn.pack(side="left")

    def append_text(self, widget, text):
        widget.config(state="normal")
        widget.insert(tk.END, text + "\n\n")
        widget.see(tk.END)
        widget.config(state="disabled")

    def send_message(self, event=None):
        user_text = self.input_box.get().strip()
        if not user_text:
            return

        self.input_box.delete(0, tk.END)

        self.append_text(self.eliza_chat, f"You: {user_text}")
        self.append_text(self.llm_chat, f"You: {user_text}")

        # ELIZA is fast, so call directly
        eliza_reply = get_eliza_response(user_text)
        self.append_text(self.eliza_chat, f"ELIZA: {eliza_reply}")

        # LLM can be slow, so run in background
        self.append_text(self.llm_chat, "LLM: Thinking...")

        threading.Thread(
            target=self.get_llm_in_background,
            args=(user_text,),
            daemon=True
        ).start()

    def get_llm_in_background(self, user_text):
        try:
            llm_reply = get_llm_response(user_text)
        except Exception as e:
            llm_reply = f"[Error: {e}]"

        self.root.after(0, self.replace_last_llm_message, llm_reply)

    def replace_last_llm_message(self, new_text):
        self.llm_chat.config(state="normal")
        content = self.llm_chat.get("1.0", tk.END).rstrip()

        marker = "LLM: Thinking..."
        if content.endswith(marker):
            content = content[:-len(marker)].rstrip()

        self.llm_chat.delete("1.0", tk.END)
        self.llm_chat.insert(tk.END, content + "\n\n")
        self.llm_chat.insert(tk.END, f"LLM: {new_text}\n\n")
        self.llm_chat.see(tk.END)
        self.llm_chat.config(state="disabled")

    def clear_chats(self):
        for widget, starter in [
            (self.eliza_chat, "ELIZA ready.\n\n"),
            (self.llm_chat, "LLM ready.\n\n")
        ]:
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, starter)
            widget.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatComparisonGUI(root)
    root.mainloop()