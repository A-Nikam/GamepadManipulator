import pygame
import serial
import time
import sys

# --- Configuration ---
SERIAL_PORT = 'COM4'  # !! Verify Correct Port !!
BAUD_RATE = 115200
# Thresholds
TRIGGER_THRESHOLD = 0.5  # Axis 4 Trigger press threshold (-1.0 to 1.0)
# Timing & Steps
COMMAND_INTERVAL = 0.05  # Send command every 50ms (20 Hz)
BASE_STEP_DEG = 2        # Degrees to move base servo per D-pad press interval
SHOULDER_STEP_DEG = 2    # Degrees to move shoulder servo per D-pad press interval
ELBOW_STEP_DEG = 2       # Degrees to move elbow servo per button press interval

# Replay/Recording feature: button index for toggling record (X button)
RECORD_BUTTON_INDEX = 2  # X Button

# --- URDF Limits (Radians) ---
BASE_MIN_RAD = -1.57
BASE_MAX_RAD = 1.57  # +/- 90deg for 180deg servo
SHOULDER_MIN_RAD = -0.785
SHOULDER_MAX_RAD = 0.873
ELBOW_MIN_RAD = -0.785
ELBOW_MAX_RAD = 2.356
MAX_STATUS_LINE_LENGTH = 50
# --- Servo Limits (Degrees) ---
SERVO_MIN_DEG = 0
SERVO_MAX_DEG = 180

# --- Initial State (Radians -> Degrees, Mapped to Servo) ---
INITIAL_BASE_RAD = 0.0
INITIAL_SHOULDER_RAD = 0.0
INITIAL_ELBOW_RAD = 2.356

# --- Helper to map radians to servo degrees ---
def map_rad_to_servo(rad_val, rad_min, rad_max, servo_min=SERVO_MIN_DEG, servo_max=SERVO_MAX_DEG):
    rad_val = max(rad_min, min(rad_max, rad_val))
    rad_range = rad_max - rad_min
    servo_range = servo_max - servo_min
    if rad_range == 0: return servo_min
    mapped = (((rad_val - rad_min) * servo_range) / rad_range) + servo_min
    return int(max(servo_min, min(servo_max, mapped)))

# Compute initial servo angles
def compute_initials():
    b = map_rad_to_servo(INITIAL_BASE_RAD, BASE_MIN_RAD, BASE_MAX_RAD)
    s = map_rad_to_servo(INITIAL_SHOULDER_RAD, SHOULDER_MIN_RAD, SHOULDER_MAX_RAD, 0, 95)
    e = map_rad_to_servo(INITIAL_ELBOW_RAD, ELBOW_MIN_RAD, ELBOW_MAX_RAD)
    return {'base': b, 'shoulder': s, 'elbow': e}

initial_angles = compute_initials()

base_servo_min, base_servo_max = SERVO_MIN_DEG, SERVO_MAX_DEG
shoulder_servo_min, shoulder_servo_max = 0, 95
elbow_servo_min, elbow_servo_max = SERVO_MIN_DEG, SERVO_MAX_DEG

print(f"Initial Servo Angles: {initial_angles}")

# Current angles start at initial
current_angles = dict(initial_angles)

# Recording state
recording = False
recorded_commands = []
new_initial = dict(initial_angles)
prev_record_button = False

# Initialize Pygame and joystick
pygame.init(); pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("Error: No joystick detected!"); sys.exit()
joystick = pygame.joystick.Joystick(0); joystick.init()
print(f"Joystick: {joystick.get_name()}")

# Initialize Serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    # Reset device lines
    ser.dtr = False; ser.rts = False; time.sleep(0.1)
    ser.dtr = True; ser.rts = True; time.sleep(1.5)
    ser.flushInput()
    print(f"Serial open on {SERIAL_PORT}")
except Exception as e:
    print(f"Serial error: {e}"); pygame.quit(); sys.exit()

last_time = time.time()
print("Ready. Press X to start/stop recording, Ctrl+C to quit.")

try:
    while True:
        # Event pump
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: raise KeyboardInterrupt

        # Throttle loop
        now = time.time()
        if now - last_time < COMMAND_INTERVAL:
            time.sleep(0.005); continue
        last_time = now

        # Read inputs
        dpad = joystick.get_hat(0) if joystick.get_numhats()>0 else (0,0)
        btn_up = joystick.get_button(3)    # Y
        btn_down = joystick.get_button(0)  # A
        btn_record = joystick.get_button(RECORD_BUTTON_INDEX)
        trigger = joystick.get_axis(4)

        # Toggle record on button edge
        if btn_record and not prev_record_button:
            if not recording:
                recording = True
                recorded_commands.clear()
                new_initial = dict(current_angles)
                print("Recording started...", end='\r')
            else:
                recording = False
                print("Recording stopped. Playing back...", end='\r')
                # Return to new initial
                init_cmd = f"S0:{new_initial['base']},S1:{new_initial['shoulder']},S2:{new_initial['elbow']}\n"
                ser.write(init_cmd.encode()); time.sleep(0.5)
                # Playback all recorded
                for cmd in recorded_commands:
                    ser.write(cmd.encode()); time.sleep(COMMAND_INTERVAL)
                print("Playback complete.", end='\r')
        prev_record_button = btn_record

        # Check reset trigger
        if trigger > TRIGGER_THRESHOLD:
            current_angles = dict(initial_angles)
            print("Reset to home.", end='\r')
        else:
            # Apply movement
            if dpad[1] == 1: current_angles['shoulder'] += SHOULDER_STEP_DEG
            elif dpad[1] == -1: current_angles['shoulder'] -= SHOULDER_STEP_DEG
            elif dpad[0] == -1: current_angles['base'] -= BASE_STEP_DEG
            elif dpad[0] == 1: current_angles['base'] += BASE_STEP_DEG
            elif btn_up: current_angles['elbow'] += ELBOW_STEP_DEG
            elif btn_down: current_angles['elbow'] -= ELBOW_STEP_DEG

        # Clamp to limits
        current_angles['base'] = max(base_servo_min, min(base_servo_max, current_angles['base']))
        current_angles['shoulder'] = max(shoulder_servo_min, min(shoulder_servo_max, current_angles['shoulder']))
        current_angles['elbow'] = max(elbow_servo_min, min(elbow_servo_max, current_angles['elbow']))

        # Send command
        cmd = f"S0:{current_angles['base']},S1:{current_angles['shoulder']},S2:{current_angles['elbow']}\n"
        ser.write(cmd.encode())

        # If recording, save command
        if recording:
            recorded_commands.append(cmd)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close(); pygame.quit();
    print("Cleanup done.")