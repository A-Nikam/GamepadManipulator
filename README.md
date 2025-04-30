# GamepadManipulator

Welcome to **GamepadManipulator**! This project offers a **3-Degree-of-Freedom (DOF)** robotic arm controlled using an Xbox gamepad. Think of it as a miniature version of the manipulator arms used in satellite docking.

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
- **Python 3.x** installed, along with the following packages:
  ```bash
  pip install pygame pyserial
