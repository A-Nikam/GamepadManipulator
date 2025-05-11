# GamepadManipulator

This project presents a **3 Degree of Freedom (DOF) robotic manipulator** system controllable via an Xbox gamepad. It demonstrates real-time joint control and includes a feature for recording and replaying movement sequences. The system architecture involves a Python script for input processing and control logic, communicating serially with an Arduino Uno that directly drives the manipulator's servo motors. This project was inspired by the control principles used in robotic arms for tasks such as satellite docking.

---

## Features
- Full three-axis control: **Base yaw**, **Shoulder pitch**, and **Elbow pitch**, all managed via your Xbox controller through Pygame.
- Seamless communication between your laptop and Arduino via USB at a baud rate of **115200**.
- Precise position control for intuitive and responsive movements.

---

## Hardware Requirements
To get started, you’ll need the following:
- A **3 DOF arm frame** (either 3D-printed or a kit).
- An **Arduino Uno** (mini or standard version).
- **Two MG995 servos** for the shoulder and elbow joints.
- **One MG90S servo** for the base.
- An **Xbox controller** (or any Pygame-compatible gamepad).

---

## Software Requirements
On your laptop, make sure you have:
- **Python 3.13.3** installed, along with the following packages:
- **Pygame Library:** Used for reading gamepad inputs. Install via pip:
  ```bash
  pip isntall pygame
  ```
- **PySerial Library:** Used for serial communication with the Arduino. Install via pip:
  ```bash
  pip install pyserial
  ```
- **Arduino IDE:** Required for compiling and uploading the sketch to the Arduino Uno.

---

## Setup and Implementation
Follow these steps to set up and run the project:
- **Assemble Manipulator Hardware:**
     - Construct the physical arm structure.
     - Mount the MG90S servo for base rotation.
     - Install the two MG995 servos at the shoulder and elbow joints.
     - Connect the arm linkages to the servo horns, ensuring free movement within the intended range.
     - [Provide any specific assembly notes relevant to your physical build here.]
 - **Wire Electronic Components:**
   - Connect the three Li-ion batteries in series to the input of the buck converter.
   - Connect the output of the buck converter to the VCC and GND pins of all three servo motors. Warning: Do not attempt to power the servos directly from the Arduino's 5V pin, as they draw more current than it can safely supply.
   - Connect the signal pin of the Base servo (MG90S) to Arduino Digital Pin 9.
   - Connect the signal pin of the Shoulder servo (MG995) to Arduino Digital Pin 10.
   - Connect the signal pin of the Elbow servo (MG995) to Arduino Digital Pin 11.
   - Establish a common ground by connecting a GND wire from the buck converter output to an Arduino GND pin.
Connect the Arduino to your computer using the USB cable.
