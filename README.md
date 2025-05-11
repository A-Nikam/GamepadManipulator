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
   - Connect the Arduino to your computer using the USB cable.
 - **Upload Arduino Sketch:**
   - Open the arduino_code.ino file in the Arduino IDE.
   - Select the correct board (Arduino Uno) and the serial port assigned to it under the Tools menu.
   - Verify that the servo pin definitions (BASE_SERVO_PIN, SHOULDER_SERVO_PIN, ELBOW_SERVO_PIN) in the sketch match your physical wiring.
   - Confirm the SERIAL_BAUD_RATE (115200) matches the value in the Python script.
   - Compile and upload the sketch to your Arduino Uno.
 - **Install Python Libraries:**
   -Open a terminal or command prompt.
 - **Execute the following command to install the necessary Python libraries:**
   - pip install pygame pyserial
 - **Configure Python Script:**
   - Open the python_controller.py script in a text editor.
   - Essential: Update the SERIAL_PORT variable near the top of the script to the serial port assigned to your Arduino. This can be found in the Arduino IDE's Tools > Port menu (e.g., 'COM4' on Windows, '/dev/ttyACM0' or '/dev/ttyUSB0' on Linux/macOS).
   - Adjust the step size constants (BASE_STEP_DEG, SHOULDER_STEP_DEG, ELBOW_STEP_DEG) if you wish to modify the movement increment per controller input.
   - Review and fine-tune the servo limits (base_servo_min, base_servo_max, etc.) to accurately reflect the safe operational range of your physical arm and servos. Ensure these limits are consistent with the constrain values used in the Arduino sketch.

---

## Operation
Once the hardware is wired and the software is configured and running:
 - **Power On:** Ensure the servo power supply (batteries and buck converter) is active.
 - **Connect Gamepad:** Plug your Xbox controller into the computer.
 - **Run Python Script:** Execute the Python script from your terminal:
python python_controller.py

Observe the console output for initialization messages.
 - **Control Manipulator:** Use the Xbox controller inputs:
   - **D-pad Up/Down:** Controls Shoulder Pitch.
   - **D-pad Left/Right:** Controls Base Yaw.
   - **'Y' Button:** Increases Elbow Pitch angle.
   - **'A' Button:** Decreases Elbow Pitch angle.
   - **Right Trigger (Axis 4 > 0.5 threshold):** Resets the arm to the initial home position.
   - **'X' Button (Button 2):** Toggles the recording feature.
     - Press once to begin recording subsequent movements.
     - Press again to stop recording, return the arm to the recording start position, and initiate playback of the recorded sequence.
   - Terminate Script: Press Ctrl+C in the terminal running the Python script to exit the program.

  ---

## Project Structure
 - **python_controller.py:** Contains the Python script for gamepad input, control logic, recording, and serial communication.
 - **arduino_code.ino:** Contains the Arduino sketch for receiving serial commands and controlling the servo motors.
 - **modified_3dof_arm.urdf:** Unified Robot Description Format file describing the kinematic structure and visual properties of the manipulator model.

---

## URDF Model
The included modified_3dof_arm.urdf file provides a formal description of the robot's links and joints. This model was instrumental in understanding the kinematic structure and visualizing the intended joint axes and ranges of motion, which aided in the design and calibration of the physical manipulator and its control software.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
