#GamepadManipulator
Hey there! This project brings you a 3-Degree-of-Freedom robotic arm that you control with an Xbox gamepad. Think of it as a miniature version of those manipulator arms used for satellite docking. A Python script on your laptop communicates over serial with an Arduino Uno, which in turn drives the servos for the base, shoulder and elbow. There’s even a recording feature so you can capture a sequence of movements and play them back.

Features
The arm gives you three-axis control—base yaw, shoulder pitch and elbow pitch—using your Xbox controller via Pygame. Your laptop and Arduino chat at 115200 baud over USB, sending precise position commands to each servo. You can record your motions with a single button press and then replay them from the same starting position. Built-in software limits prevent the arm from exceeding its physical range, and there’s a quick-reset command to send it home instantly.

Hardware Requirements
You’ll need a 3 DOF arm frame (3D printed or kit), an Arduino Uno (mini or standard), two MG995 servos for shoulder and elbow, one MG90S servo for the base, an Xbox controller (or any Pygame-compatible gamepad), jumper wires, a USB cable, three Li-ion batteries and a buck converter to step down voltage to 5–6 V. Make sure the battery pack can supply enough current for all three servos, and always tie the servo power ground to the Arduino ground.

Software Requirements
On your laptop install Python 3.x along with the Pygame and PySerial packages (pip install pygame pyserial). You’ll also need the Arduino IDE to upload the firmware to your Uno.

Setup
First assemble your arm and mount the MG90S on the base and MG995s on the shoulder and elbow. Next wire the batteries into the buck converter input and power all three servos from the converter output—do not use the Arduino’s 5 V pin for servo power. Connect the MG90S signal line to Arduino pin 9, and the two MG995 signals to pins 10 and 11. Don’t forget to share ground between the converter and the Arduino. Finally plug the Uno into your laptop via USB.

Uploading Code
Open arduino_code.ino in the Arduino IDE. Select “Arduino Uno” and the correct serial port, verify that the pin definitions and SERIAL_BAUD_RATE (115200) match your wiring and Python script, then hit upload.

Python Controller
In your terminal, navigate to the folder containing python_controller.py. If needed, update the SERIAL_PORT constant to match your system (COM4 on Windows or /dev/ttyACM0 on Linux/macOS). You can also tweak BASE_STEP_DEG, SHOULDER_STEP_DEG, and ELBOW_STEP_DEG for finer or larger movements, and adjust the servo limit constants to suit your physical arm’s range.

Usage
Power on your servos, connect the gamepad, and run:

nginx
Copy
Edit
python python_controller.py
Use the D-pad to move the shoulder and twist the base, the Y/A buttons to bend or straighten the elbow, X to start/stop recording, and hold the right trigger to return to home. Press Ctrl + C to exit.

Code Structure
python_controller.py listens to gamepad input, computes target angles and sends serial commands, with built-in recording and playback logic.

arduino_code.ino parses incoming serial commands and drives the servos using the Arduino Servo library.

modified_3dof_arm.urdf describes the arm’s links and joints for simulation or visualization.

Future Work
Ideas for next steps include adding a wrist or gripper, integrating inverse-kinematics so you can command an end-effector position directly, porting to ROS 2 for advanced motion planning, mounting a camera for vision-based tasks, building a GUI for easier operation, saving and loading recorded sequences, and adding battery-level monitoring.

License
This project is open source under the MIT License. See the LICENSE file for details.

Thank you to everyone who helped along the way—professors, classmates and the countless online tutorials!
