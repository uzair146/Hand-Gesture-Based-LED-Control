# Hand Gesture Based LED Control

A real-time hand gesture recognition system built for the Digital Logic Design (DLD) Lab. It uses a webcam to detect how many fingers are raised and controls the corresponding number of LEDs on an Arduino via serial communication.

---

## How It Works

The Python script captures live video from the webcam and passes each frame to **MediaPipe**, which detects 21 hand landmark points. The script then counts how many fingers are extended and sends that number (0–5) to the Arduino over USB Serial. The Arduino turns on that many LEDs.

```
Webcam → MediaPipe → Finger Count → Serial → Arduino → LEDs
```

---

## Requirements

### Hardware
- Arduino Uno (or Nano)
- 5 LEDs
- 5 × 220Ω resistors
- Jumper wires
- USB cable
- Webcam or laptop camera

### Software
- Python 3.8+
- Arduino IDE

---

## Installation

**1. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**2. Upload Arduino sketch**

Open `arduino_led_control.ino` in Arduino IDE, select your board and port, then click Upload.

---

## Wiring

Connect each LED through a 220Ω resistor to its Arduino pin. Connect all cathodes (short leg) to GND.

| LED   | Arduino Pin |
|-------|-------------|
| LED 1 | Pin 2       |
| LED 2 | Pin 3       |
| LED 3 | Pin 4       |
| LED 4 | Pin 5       |
| LED 5 | Pin 6       |

---

## Usage

**Find your Arduino COM port first:**
- Windows: Device Manager → Ports (COM & LPT)
- Linux/Mac: `ls /dev/tty*` (usually `/dev/ttyUSB0`)

**Run the script:**

```bash
# With Arduino connected (default port: COM6)
python main.py

# With Arduino on a different port
python main.py --port COM3

# On Linux/Mac
python main.py --port /dev/ttyUSB0

# Without Arduino (demo mode — virtual LEDs shown on screen)
python main.py --no-arduino
```

Press `Q` to quit.

---

## Finger Detection Logic

| Finger | Method |
|--------|--------|
| Thumb | Tip X position compared to joint below it |
| Index, Middle, Ring, Pinky | Tip Y position compared to 2nd joint (tip higher = extended) |

MediaPipe assigns 21 landmark IDs to each hand. The fingertip IDs used are: **4, 8, 12, 16, 20**.

---

## Project Structure

```
├── main.py                  # Python script (webcam + finger detection + serial)
├── arduino_led_control.ino  # Arduino sketch (receives count, controls LEDs)
└── requirements.txt         # Python dependencies
```

---

## Team Members

| Name | 
|Muhammad Uzair Hussain|
|Muqarrab Mustafa |

**Course:** Digital Logic Design Lab
**Semester:** 2nd
