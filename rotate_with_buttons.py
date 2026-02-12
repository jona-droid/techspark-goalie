import tkinter as tk
from tkinter import messagebox
import serial
import time

# --- CONFIGURATION ---
serial_port = '/dev/cu.usbmodem1301'
baud_rate = 9600

# Connect to Arduino
try:
    arduino = serial.Serial(serial_port, baud_rate)
    time.sleep(2)
    print(f"Connected to {serial_port}")
except:
    print("Arduino not found! Check your port name.")
    exit()

# Create GUI window
root = tk.Tk()
root.title("Goalie Control Panel")
root.geometry("600x200")

# Current position label
position_label = tk.Label(root, text="Position: NONE", font=("Arial", 20, "bold"))
position_label.pack(pady=20)

current_position = {"value": "NONE"}

# Button functions
def send_left():
    data = b'L'
    arduino.write(data)
    print(f"Sent: {data} - Arduino responded: {len(data)} bytes written")
    current_position["value"] = "LEFT"
    position_label.config(text="Position: LEFT", fg="red")
    print("Sent: LEFT (L)")

def send_center():
    data = b'C'
    arduino.write(data)
    print(f"Sent: {data} - Arduino responded: {len(data)} bytes written")
    current_position["value"] = "CENTER"
    position_label.config(text="Position: CENTER", fg="orange")
    print("Sent: CENTER (C)")

def send_right():
    data = b'R'
    arduino.write(data)
    print(f"Sent: {data} - Arduino responded: {len(data)} bytes written")
    current_position["value"] = "RIGHT"
    position_label.config(text="Position: RIGHT", fg="green")
    print("Sent: RIGHT (R)")

# Create buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

left_btn = tk.Button(button_frame, text="LEFT", command=send_left, width=10, height=3, bg="red", fg="red", font=("Arial", 12, "bold"))
left_btn.grid(row=0, column=0, padx=10)

center_btn = tk.Button(button_frame, text="CENTER", command=send_center, width=10, height=3, bg="orange", fg="orange", font=("Arial", 12, "bold"))
center_btn.grid(row=0, column=1, padx=10)

right_btn = tk.Button(button_frame, text="RIGHT", command=send_right, width=10, height=3, bg="green", fg="green", font=("Arial", 12, "bold"))
right_btn.grid(row=0, column=2, padx=10)

# Close function
def on_closing():
    arduino.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start GUI
root.mainloop()