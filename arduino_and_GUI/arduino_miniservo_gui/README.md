# Arduino Mini Servo Control Project

## Project Overview

This project creates a GUI application to control a mini servo motor connected to an Arduino board. The system consists of two main components:
1. An Arduino sketch that receives commands and controls the servo motor.
2. A Python GUI application that sends angle commands to the Arduino.

## Hardware Setup

1. Connect the mini servo to the Arduino:
   - Red wire to 5V
   - Brown or Black wire to GND
   - Orange or Yellow wire to pin 9
2. Connect the Arduino to your computer via USB.

## Software Setup

### Arduino Setup

1. Open the Arduino IDE and upload the following sketch:

```cpp
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
}

void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt(); // read the incoming byte
    if (angle >= 0 && angle <= 180) {
      myservo.write(angle);
      Serial.print("Moved to ");
      Serial.println(angle);
    }
  }
}
```

### Python Environment Setup

1. Open Anaconda Powershell Prompt.
2. Activate your environment (or create a new one):
   ```
   conda activate arduino_env
   ```
   If you need to create a new environment:
   ```
   conda create --name arduino_env python=3.9
   conda activate arduino_env
   ```
3. Install required packages:
   ```
   conda install pyserial
   conda install tk
   ```

## Running the Application

1. Ensure your Arduino is connected and the correct sketch is uploaded.
2. Open Anaconda Powershell Prompt and activate your environment:
   ```
   conda activate arduino_env
   ```
3. Navigate to your project directory:
   ```
   cd path\to\your\project
   ```
4. Create a new Python file named `servo_control_gui.py`:
   ```
   notepad servo_control_gui.py
   ```
5. Copy and paste the following code into the file:

```python
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
        ports = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10', 'COM11', 'COM12', 'COM13']
        while True:
            for port in ports:
                try:
                    self.arduino = serial.Serial(port, 9600, timeout=1)
                    print(f"Connected to Arduino on {port}")
                    self.master.after(0, self.update_status, f"Status: Connected on {port}")
                    return
                except serial.SerialException:
                    continue
            print("Failed to connect to Arduino on any port")
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
```

6. Save the file and close Notepad.
7. Run the script:
   ```
   python servo_control_gui.py
   ```

## Usage

1. The GUI will display a slider to select the servo angle (0-180 degrees).
2. Use the slider to choose the desired angle.
3. Click the "Move Servo" button to send the command to the Arduino.
4. The servo should move to the specified angle.

## Important Notes

1. Ensure all connections are secure and correct before powering on the Arduino.
2. The current setup may cause the servo to heat up during extended use. This could be due to electrical noise causing the motor to continue working even when not actively moving. Consider the following precautions:
   - Limit continuous operation time to prevent overheating.
   - Implement a cooldown period between movements.
   - Consider adding a capacitor across the power lines to reduce electrical noise.
   - Ensure the power supply is adequate for the servo's requirements.
3. If you encounter connection issues, try unplugging and replugging the Arduino, then restart the Python script.
4. The GUI will continuously attempt to reconnect if the connection is lost.
5. Make sure no other programs (including the Arduino IDE) are using the serial port when running the Python script.

## Future Improvements

To address the heating issue and improve overall performance, consider the following enhancements:
1. Implement a power-saving mode that disengages the servo when not in use.
2. Add better error handling and feedback in both the Arduino sketch and Python script.
3. Optimize the communication protocol to reduce unnecessary commands.
4. Explore using a servo library that provides more precise control and potentially reduces power consumption.

Remember to always monitor the servo's temperature during operation and discontinue use if it becomes excessively hot.