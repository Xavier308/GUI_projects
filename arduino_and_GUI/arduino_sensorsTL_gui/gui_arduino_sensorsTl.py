import tkinter as tk
import serial
import threading
import re

# Global variables
arduino = None
temperature_value = None
light_value = None

def start_arduino_connection():
    global arduino
    try:
        arduino = serial.Serial('COM13', 9600, timeout=1)  # Change COM3 to your Arduino port
        print("Connected to Arduino successfully")
        return True
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        return False

def read_from_arduino():
    global arduino, temperature_value, light_value
    if not arduino or not arduino.is_open:
        print("Arduino is not connected")
        return

    try:
        while True:
            data = arduino.readline().decode().strip()
            if data:
                print(f"Received data: {data}")
                match = re.search(r"Temperature: (\d+), Light: (\d+)", data)
                if match:
                    temp, light = match.groups()
                    temperature_value.set(f"Temperature: {temp}")
                    light_value.set(f"Light: {light}")
    except serial.SerialException as e:
        print(f"Error reading from Arduino: {e}")
        temperature_value.set("Error: Lost connection to Arduino")
        light_value.set("Error: Lost connection to Arduino")

def start_reading():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

def main():
    global temperature_value, light_value
    root = tk.Tk()
    root.title("Arduino Sensor Reader")
    root.geometry('400x300')

    temperature_value = tk.StringVar()
    temperature_value.set("Waiting for temperature data...")
    light_value = tk.StringVar()
    light_value.set("Waiting for light data...")

    if start_arduino_connection():
        temp_label = tk.Label(root, textvariable=temperature_value)
        temp_label.pack(pady=20)

        light_label = tk.Label(root, textvariable=light_value)
        light_label.pack(pady=20)

        start_reading()
    else:
        error_label = tk.Label(root, text="Failed to connect to Arduino. Check your connection and try again.")
        error_label.pack(pady=20)

    root.mainloop()

    if arduino and arduino.is_open:
        arduino.close()

if __name__ == "__main__":
    main()
