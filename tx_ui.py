import serial
import tkinter as tk
from tkinter import messagebox, scrolledtext
import time

# --- Configuration ---
PORT = "COM13"        # change to your Pico port
BAUD_RATE = 115200

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"✅ Connected to {PORT}")
except serial.SerialException:
    messagebox.showerror("Connection Error", f"Could not open {PORT}. Check connection or port name.")
    exit()

# --- Functions ---
def send_message(event=None):
    msg = entry.get().strip()
    if not msg:
        return
    try:
        ser.write((msg + "\n").encode())
        add_message("You", msg, "green")
        entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Send Error", str(e))

def add_message(sender, text, color):
    bubble = tk.Frame(chat_frame, bg=color, padx=10, pady=5)
    msg_label = tk.Label(
        bubble,
        text=f"{sender}: {text}",
        font=("Segoe UI", 11),
        bg=color,
        fg="black" if color != "limegreen" else "white",
        wraplength=350,
        justify="left",
    )
    msg_label.pack()
    bubble.pack(anchor="e" if sender == "You" else "w", pady=3, padx=10)
    canvas.update_idletasks()
    canvas.yview_moveto(1)

def exit_program():
    try:
        ser.write(b"exit\n")
        ser.close()
    except:
        pass
    root.destroy()

# --- UI Setup ---
root = tk.Tk()
root.title("Optical Chat - Transmitter")
root.geometry("420x500")
root.configure(bg="#101010")

title = tk.Label(root, text="💬 Optical Chat - You", font=("Segoe UI", 14, "bold"),
                 bg="#202020", fg="white", pady=10)
title.pack(fill=tk.X)

# Scrollable chat area
chat_frame_outer = tk.Frame(root, bg="#101010")
chat_frame_outer.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

canvas = tk.Canvas(chat_frame_outer, bg="#101010", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame_outer, command=canvas.yview)
chat_frame = tk.Frame(canvas, bg="#101010")

chat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=chat_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Entry + Send button
entry_frame = tk.Frame(root, bg="#101010")
entry_frame.pack(fill=tk.X, padx=10, pady=5)

entry = tk.Entry(entry_frame, font=("Segoe UI", 12), bg="#181818", fg="white", insertbackground="white")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", send_message)

send_btn = tk.Button(entry_frame, text="Send", bg="limegreen", fg="white",
                     font=("Segoe UI", 11, "bold"), width=8, command=send_message)
send_btn.pack(side=tk.RIGHT)

exit_btn = tk.Button(root, text="Exit", bg="#ff5555", fg="white",
                     font=("Segoe UI", 11, "bold"), command=exit_program)
exit_btn.pack(pady=5)

root.mainloop()
