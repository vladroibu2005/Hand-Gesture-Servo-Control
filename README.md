A real-time computer vision and embedded systems project that uses MediaPipe hand tracking to control an SG90 servo motor through an ESP32.

## Project Description

This project implements a real-time gesture-based servo motor control system using **Python, OpenCV, MediaPipe, and an ESP32**. The horizontal position of the user's index fingertip is detected through a webcam and mapped to a servo motor angle between **0° and 180°**.

The system combines computer vision, coordinate processing, serial communication, and embedded hardware control into a single interactive application.

### How It Works

The system follows this processing pipeline:

**Webcam → OpenCV → MediaPipe Hand Tracking → Landmark Detection → Coordinate Extraction → Angle Mapping → Serial Communication → ESP32 → SG90 Servo Motor**

### 1. Webcam Capture

The system uses OpenCV to continuously capture frames from the computer's webcam.

Each frame is:

* captured from the camera;
* horizontally flipped to provide a mirror-like interaction;
* converted from **BGR to RGB**, as required by MediaPipe.

The webcam is configured to provide a real-time video stream that is processed frame by frame.

### 2. Hand Detection and Landmark Tracking

MediaPipe's **Hand Landmarker** is used to detect and track the user's hand.

For each detected hand, MediaPipe provides **21 landmarks**, each containing normalized `x`, `y`, and `z` coordinates.

The project is mainly interested in:

* Landmark `0` — wrist
* Landmark `5` — index finger MCP joint
* Landmark `8` — index fingertip
* Landmark `12` — middle fingertip

The index fingertip (landmark `8`) is used as the main control point.

### 3. Converting Normalized Coordinates to Pixels

MediaPipe provides normalized coordinates in the range `[0, 1]`.

These coordinates are converted into pixel coordinates based on the current frame dimensions:

```python
x = int(point.x * w)
y = int(point.y * h)
```

This allows the fingertip position to be displayed directly on the OpenCV image and used for further calculations.

### 4. Extracting the Index Fingertip Position

The coordinates of all detected landmarks are stored in a dictionary using their landmark IDs.

The project then retrieves landmark `8`:

```python
x8, y8 = coordonate_puncte[8]
```

The resulting `x8` coordinate represents the horizontal position of the index fingertip within the camera frame.

### 5. Mapping Hand Position to Servo Angle

The horizontal fingertip position is converted into a servo angle between **0° and 180°**.

The mapping is based on the width of the camera frame:

```python
angle = int(x8 / w * 180)
```

Therefore:

* the left side of the frame corresponds approximately to **0°**;
* the center corresponds approximately to **90°**;
* the right side corresponds approximately to **180°**.

This creates a virtual horizontal slider controlled by the user's index finger.

### 6. Virtual Slider Visualization

An on-screen slider is rendered using OpenCV to provide visual feedback.

The slider represents the complete servo operating range:

```text
0° ─────────────────────────────── 180°
        ↑
   Current position
```

The position of the slider indicator is calculated from the current servo angle, allowing the user to see the relationship between hand movement and servo position in real time.

The application also displays:

* fingertip X coordinate;
* fingertip Y coordinate;
* calculated servo angle;
* current position on the virtual slider.

### 7. Serial Communication

The calculated angle is transmitted from Python to the ESP32 through a serial connection at **115200 baud**.

Instead of sending the angle as a text string, the project sends it as a single byte:

```python
esp32.write(angle.to_bytes(1, 'little'))
```

Since the servo angle is limited to `0–180`, the complete value can be represented by one byte.

This provides a simple communication protocol between the Python application and the embedded controller.

### 8. ESP32 Servo Control

The ESP32 receives the byte sent by the Python application through its serial interface.

The received value is interpreted as the desired servo angle and passed to the servo control function:

```cpp
int angle = Serial.read();

if (angle >= 0 && angle <= 180) {
    servo.write(angle);
}
```

The SG90 servo is connected to a digital GPIO configured for servo control.

The ESP32 therefore acts as the hardware interface between the computer vision application and the physical actuator.

### 9. Physical Output

The final output is an **SG90 positional servo motor**.

Moving the index finger horizontally across the camera frame changes the calculated angle, which is transmitted to the ESP32 and applied to the servo.

The result is a real-time interaction in which:

**moving the finger left → servo moves toward 0°**

**moving the finger to the center → servo moves toward 90°**

**moving the finger right → servo moves toward 180°**

### Technologies Used

* **Python 3**
* **OpenCV**
* **MediaPipe**
* **PySerial**
* **ESP32**
* **Arduino IDE**
* **ESP32Servo**
* **SG90 Servo Motor**

### Key Concepts Implemented

This project combines several concepts from computer vision and embedded systems:

* Real-time webcam processing
* Hand detection and tracking
* MediaPipe hand landmarks
* Normalized-to-pixel coordinate conversion
* Coordinate-based control
* Linear value mapping
* Serial communication
* ESP32 programming
* Servo motor control
* Python-to-microcontroller communication
* Computer vision to physical actuator integration



