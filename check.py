import tkinter as tk
from tkinter import ttk
import threading
from checker import WalletChecker
from PIL import Image, ImageTk
import os
import getpass
import json

class WalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scan Wallet Cryto")

        icon_path = os.path.join(os.path.dirname(__file__), "images", "logo.ico")
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print("Cannot set icon:", e)

        self.checker = WalletChecker(self.update_log, self.update_stats)
        self.running = False

        pass_frame = tk.Frame(root)
        pass_frame.pack(pady=5)

        tk.Label(pass_frame, text="Pass:").pack(side=tk.LEFT, padx=(5, 0))

        self.pass_entry = tk.Entry(pass_frame, show="*", width=100)
        self.pass_entry.pack(side=tk.LEFT, padx=5)

        self.accept_buton = tk.Button(pass_frame, text="Accept", command=self.accept_pass)
        self.accept_buton.pack(side=tk.LEFT)

        self.pass_verified = False

        self.log_text = tk.Text(root, height=20, bg="black", fg="white")
        self.log_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        stats_frame = tk.Frame(root)
        stats_frame.pack(pady=5)

        self.stats_label = tk.Label(stats_frame, text="Checked: 0", font=("Helvetica", 14, "bold"))
        self.stats_label.pack(anchor="w", padx=10)

        readonly_label = tk.Label(stats_frame, text="Found", font=("Helvetica", 10, "bold"))
        readonly_label.pack(anchor="w", padx=10)

        self.readonly_note = tk.Text(stats_frame, font=("Helvetica", 12), height=3, wrap="word", fg="green", bg="#f0f0f0")
        self.readonly_note.pack(pady=(0, 5), fill=tk.X, padx=10)

        self.readonly_note.insert(tk.END, "")

        chain_frame = tk.LabelFrame(root, text="")
        chain_frame.pack(padx=10, pady=5)

        self.chains = {
            'ETH': tk.BooleanVar(value=True),
            'BNB': tk.BooleanVar(value=True),
            'USDT': tk.BooleanVar(value=True),
            'LTC': tk.BooleanVar(value=True),
            'SOL': tk.BooleanVar(value=True),
            'BTC': tk.BooleanVar(value=True),
        }

        self.chains_images = {}

        image_folder = os.path.join(os.path.dirname(__file__), "images")

        for chains in self.chains.keys():
            try:
                image_path = os.path.join(image_folder, f"{chains.lower()}.png")
                img = Image.open(image_path).resize((30, 30))
                self.chains_images[chains] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Unable to load image for {chains}: {e}")
                self.chains_images[chains] = None

        for chain, var in self.chains.items():
            cb = tk.Checkbutton(
                chain_frame,
                text=chain,
                variable=var,
                image=self.chains_images[chain],
                compound="top",
                padx=10,
                pady=5
            )
            cb.pack(side=tk.LEFT, padx=10)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        self.start_button = tk.Button(control_frame, text="🟩 Start", bg="green", command=self.start_checking, fg="white", padx="20", pady="10")
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(control_frame, text="🟥 Stop", bg="tomato", command=self.stop_checking, fg="black", padx="20", pady="10", state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10)

        self.start_button.config(state="disabled")
        self.stop_button.config(state="disabled")

        self.telegram_label = tk.Label(root, text="Join us on Telegram: https://t.me/CheckScanWallet", font=("Helvetica", 10), fg="blue", cursor="hand2")
        self.telegram_label.pack(pady=5)
        self.telegram_label.bind("<Button-1>", self.open_telegram_link)

    def open_telegram_link(self, event):
        import webbrowser
        webbrowser.open("https://t.me/CheckScanWallet")

    def update_log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def update_stats(self, checked, total):
        self.stats_label.config(text=f"Checked: {checked}")

    def start_checking(self):
        if not self.pass_verified:
            self.update_log("Please enter correct pass before starting.")
            return

        if self.running or not self.pass_verified:
            return
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        selected_chains = [chain for chain, var in self.chains.items() if var.get()]
        self.checker.set_chains(selected_chains)
        threading.Thread(target=self.checker_runner, daemon=True).start()

    def checker_runner(self):
        self.checker.run()
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def stop_checking(self):
        self.checker.stop()
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def accept_pass(self):
        entered_pass = self.pass_entry.get().strip()
        user_id = getpass.getuser()

        pass_file = os.path.join(os.path.dirname(__file__), "passwords.json")

        if not os.path.exists(pass_file):
            self.update_log("passwords file not found.")
            return
        
        with open(pass_file, "r") as file:
            passwords = json.load(file)

        if entered_pass in passwords:
            owner = passwords[entered_pass]

            if owner is None:
                passwords[entered_pass] = {"username": user_id}
                with open(pass_file, 'w') as file:
                    json.dump(passwords, file, indent=4)
                self.pass_verified = True
                self.update_log("pass accepted and assigned to you.")
                self.start_button.config(state="normal")
            elif owner["username"] == user_id:
                self.pass_verified = True
                self.update_log("Welcome back. Pass accepted.")
                self.start_button.config(state="normal")
            else:
                self.update_log("This pass has been used by another user.")
                self.start_button.config(state="disabled")

        else:
            self.update_log("Invalid pass.")
            self.start_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletApp(root)
    root.mainloop()
