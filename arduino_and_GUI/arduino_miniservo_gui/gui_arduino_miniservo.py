import tkinter as tk
from tkinter import ttk
import serial
import threading
import time

class ServoControlGUI:
    def __init__(self, master):
        self.master = master
        master.title("Servo Control")

        self.arduino = None
        self.connection_status = tk.StringVar()
        self.connection_status.set("Status: Connecting...")

        self.angle = tk.IntVar()
        self.angle.set(90)  # Start at 90 degrees

        self.angle_slider = ttk.Scale(master, from_=0, to=180, orient="horizontal", 
                                      variable=self.angle, command=self.update_angle_label)
        self.angle_slider.pack(pady=20)

        self.angle_label = ttk.Label(master, text="Angle: 90°")
        self.angle_label.pack(pady=10)

        self.move_button = ttk.Button(master, text="Move Servo", command=self.move_servo)
        self.move_button.pack(pady=20)

        self.status_label = ttk.Label(master, textvariable=self.connection_status)
        self.status_label.pack(pady=10)

        self.connect_thread = threading.Thread(target=self.connect_to_arduino)
        self.connect_thread.start()

    def connect_to_arduino(self):
        while True:
            try:
                self.arduino = serial.Serial('COM13', 9600, timeout=1)
                print("Connected to Arduino")
                self.master.after(0, self.update_status, "Status: Connected")
                break
            except serial.SerialException as e:
                print(f"Failed to connect to Arduino: {e}")
                self.master.after(0, self.update_status, "Status: Connection failed. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before trying again

    def update_status(self, status):
        self.connection_status.set(status)

    def update_angle_label(self, event=None):
        self.angle_label.config(text=f"Angle: {self.angle.get()}°")

    def move_servo(self):
        if self.arduino and self.arduino.is_open:
            angle = self.angle.get()
            self.arduino.write(f"{angle}\n".encode())
            print(f"Sent angle: {angle}")
        else:
            print("Arduino not connected")
            self.update_status("Status: Not connected. Reconnecting...")
            self.connect_thread = threading.Thread(target=self.connect_to_arduino)
            self.connect_thread.start()

    def __del__(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()

root = tk.Tk()
gui = ServoControlGUI(root)
root.mainloop()