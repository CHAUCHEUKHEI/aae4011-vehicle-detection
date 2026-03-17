# AAE4011 Assignment 1 — ROS-Based Vehicle Detection

---

## Overview

This ROS package extracts image frames from a provided `.bag` file and runs
real-time vehicle detection using **YOLOv8**. Detected vehicles (cars, buses,
trucks, motorcycles) are displayed with bounding boxes, class labels, and
confidence scores in an OpenCV window.

---

## Video Demonstration

https://youtu.be/EATKluoEjqk

---

## Detection Method

**Model:** YOLOv8n (You Only Look Once, version 8, nano variant)  
**Library:** Ultralytics  
**Image topic:** `/hikcamera/image_2/compressed`  
**Frames extracted:** 1142  

YOLOv8 is a single-stage CNN-based object detector that predicts bounding boxes
and class probabilities in one forward pass. It was chosen because:

1. **Speed** — the nano variant runs in real-time even on a laptop CPU.
2. **Pre-trained weights** — trained on COCO (80 classes including cars, buses,
   trucks, motorcycles), so no custom training is needed.
3. **Ease of use** — a single pip install gives access to the full API with
   automatic weight download.

Vehicle classes detected (COCO IDs): car (2), motorcycle (3), bus (5), truck (7).

---

## Repository Structure
```
aae4011-vehicle-detection/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── detect.launch
├── scripts/
│   ├── extract_frames.py
│   └── detect_vehicles.py
└── README.md
```

---

## Requirements

| Dependency | Install |
|---|---|
| Python 3.8+ | included with Ubuntu |
| ultralytics | `pip3 install ultralytics` |
| opencv-python | `pip3 install opencv-python` |
| rosbags | `pip3 install rosbags` |

---

## How to Run

### Step 1 — Install dependencies
```bash
pip3 install ultralytics opencv-python rosbags --break-system-packages
```

### Step 2 — Extract frames from rosbag
```bash
python3 scripts/extract_frames.py \
  --bag /path/to/your.bag \
  --output /tmp/aae4011_frames
```

### Step 3 — Run vehicle detection
```bash
python3 scripts/detect_vehicles.py
```

**Controls:**
- `SPACE` — pause / resume
- `Q` or `ESC` — quit

---

## Q3.3 Reflection

### (a) What did I learn?

First of all, I learned how to work with ROS bag files — understanding how sensor 
data is stored in topics and how to extract image frames from them using the rosbags 
Python library. Second, I learned how to apply a pre-trained deep learning model (YOLOv8) to
real camera footage, including how confidence thresholds affect detection results.

### (b) How did I use AI tools?

I used Claude as an AI assistant to generate the core Python scripts
and guide the environment setup step by step. Rather than writing the code from 
scratch, my role was to run each step, interpret the errors that appeared, 
provide the actual outputs back to the AI, and make decisions about which 
approach to take when things failed — for example, switching from VirtualBox to 
WSL2 when the hypervisor error appeared, and switching from rosbag to rosbags 
when ROS failed to install on Ubuntu 24. Through this iterative process of 
running, failing, and fixing, I developed an understanding of how the pipeline 
works even though I did not write the code independently. The benefit of this 
approach was being able to complete a complex ROS pipeline as a beginner. The 
limitation is that my ability to modify or extend the code independently is still 
developing.

### (c) How to improve accuracy?

**Strategy 1 — Use a larger YOLOv8 model (yolov8m or yolov8l)**  
The nano model trades accuracy for speed. A medium or large variant has more
parameters and achieves higher mAP on COCO, especially for small or partially
occluded vehicles in aerial or dashcam imagery.

**Strategy 2 — Fine-tune on UAV/dashcam vehicle datasets**  
YOLOv8n is pre-trained on ground-level COCO images. Fine-tuning on datasets
which contain aerial and traffic camera viewpoints would significantly 
improve detection accuracy for this specific use case.

### (d) Real-world deployment challenges

**Challenge 1 — Computational constraints on a drone**  
Drones have strict weight and power budgets. Running a full YOLOv8 model
requires either a lightweight companion computer such as a Jetson Nano or
model quantisation (INT8), both of which add engineering complexity and may
reduce accuracy.

**Challenge 2 — Motion blur and lighting variation**  
A moving drone produces blurred frames and experiences much rapid changes in lighting
conditions. This degrades detection confidence and can cause missed detections,
requiring pre-processing steps like deblurring or exposure compensation before
inference.

---
