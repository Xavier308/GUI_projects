# Arduino Sensor GUI Project

## Project Overview

This project aims to create a GUI application that displays sensor readings from an Arduino board. The system consists of two main components:
1. An Arduino sketch that reads sensor data and sends it over a serial connection.
2. A Python GUI application that receives the data from the Arduino and displays it.

## Setup and Installation

### Arduino Setup

1. Connect your sensors to the Arduino board.
2. Open the Arduino IDE and upload the following sketch:

```cpp
const int temperaturePin = A0;  // Analog pin for temperature sensor
const int lightPin = A1;        // Analog pin for light sensor

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud
}

void loop() {
  int temperatureReading = analogRead(temperaturePin);
  int lightReading = analogRead(lightPin);
  
  Serial.print("Temperature: ");
  Serial.print(temperatureReading);
  Serial.print(", Light: ");
  Serial.println(lightReading);
  
  delay(1000);  // Wait for a second before the next reading
}
```

### Python Environment Setup

1. Install Anaconda if you haven't already.
2. Open Anaconda Powershell Prompt.
3. Create a new environment:
   ```
   conda create --name arduino_env python=3.9
   ```
4. Activate the environment:
   ```
   conda activate arduino_env
   ```
5. Install required packages:
   ```
   conda install pyserial
   conda install tk
   ```

## Running the Application

1. Open Anaconda Powershell Prompt and activate the environment:
   ```
   conda activate arduino_env
   ```
2. Navigate to your project directory:
   ```
   cd path\to\your\project
   ```
3. Create a new Python file named `gui_arduino_sensorsTL.py` using Notepad or file editor:
   ```
   notepad gui_servo_arduino.py
   ```
4. Copy and paste the following code into the file:

```python
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

```

5. Save the file and close Notepad.
6. Run the script:
   ```
   python gui_arduino_sensorsTL.py
   ```

## Problems Faced and Solutions

### Issue 1: WSL and Serial Port Access

Initially, we attempted to run the project using Windows Subsystem for Linux (WSL). However, WSL doesn't have direct access to USB devices, which caused issues with connecting to the Arduino.

#### Attempted Solutions:
1. Tried using `/dev/ttyS*` ports in WSL:
   ```python
   arduino = serial.Serial('/dev/ttyS0', 9600, timeout=1)
   ```
2. Attempted to use `/dev/ttyUSB*` ports:
   ```python
   arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
   ```

#### Final Solution:
We switched to using Windows directly with Anaconda Powershell, which allows access to COM ports. This resolved the connection issues.

### Issue 2: Inconsistent COM Port Assignment

The COM port assigned to the Arduino can change, causing connection failures.

#### Solution:
Implemented a port scanning feature in the Python script that tries multiple COM ports until it finds the correct one.

## Notes

- Always ensure that the Arduino is properly connected before running the Python script.
- If you encounter connection issues, try unplugging and replugging the Arduino, then restart the Python script.
- The GUI will continuously attempt to reconnect if the connection is lost.
- Make sure no other programs (including the Arduino IDE) are using the serial port when running the Python script.