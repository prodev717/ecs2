import serial
import tkinter as tk
from threading import Thread

PORT = "COM12"       # change to your Pico port
BAUD_RATE = 115200

ser = serial.Serial(PORT, BAUD_RATE)

# --- Functions ---
def read_from_pico():
    buffer = ""
    while True:
        if ser.in_waiting > 0:
            data = ser.read().decode(errors='ignore')
            if data == "\n":
                if buffer.strip():
                    add_message("Pico", buffer.strip(), "gray")
                buffer = ""
            else:
                buffer += data

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
    bubble.pack(anchor="w", pady=3, padx=10)
    canvas.update_idletasks()
    canvas.yview_moveto(1)

def start_reader():
    thread = Thread(target=read_from_pico, daemon=True)
    thread.start()

# --- UI Setup ---
root = tk.Tk()
root.title("Optical Chat - Receiver")
root.geometry("420x500")
root.configure(bg="#101010")

title = tk.Label(root, text="💬 Optical Chat - Pico", font=("Segoe UI", 14, "bold"),
                 bg="#202020", fg="white", pady=10)
title.pack(fill=tk.X)

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

start_reader()
root.mainloop()
