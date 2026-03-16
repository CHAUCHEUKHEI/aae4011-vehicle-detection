import os, glob, cv2, time
from collections import defaultdict
from ultralytics import YOLO

VEHICLE_CLASSES = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
COLORS = {'car': (0,200,100), 'motorcycle': (0,140,255), 'bus': (255,100,0), 'truck': (0,80,220)}

def run_detection(frames_dir):
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
    print(f"Found {len(frame_files)} frames")
    model = YOLO('yolov8n.pt')
    print("Model loaded! Starting detection...")
    print("Controls: Q = quit   SPACE = pause")
    cv2.namedWindow("AAE4011 Vehicle Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AAE4011 Vehicle Detection", 1280, 720)
    paused = False
    idx = 0
    while idx < len(frame_files):
        if not paused:
            frame = cv2.imread(frame_files[idx])
            results = model(frame, conf=0.3, verbose=False)
            counts = defaultdict(int)
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    if cls_id not in VEHICLE_CLASSES:
                        continue
                    conf = float(box.conf[0])
                    label = VEHICLE_CLASSES[cls_id]
                    color = COLORS[label]
                    x1,y1,x2,y2 = map(int, box.xyxy[0])
                    counts[label] += 1
                    cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
                    text = f"{label} {conf:.2f}"
                    (tw,th),_ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    cv2.rectangle(frame, (x1,y1-th-8), (x1+tw+4,y1), color, -1)
                    cv2.putText(frame, text, (x1+2,y1-4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            h,w = frame.shape[:2]
            cv2.rectangle(frame, (8,8), (260,90), (20,20,20), -1)
            cv2.putText(frame, f"Frame: {idx+1}/{len(frame_files)}", (14,30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (220,220,220), 1)
            cv2.putText(frame, f"Vehicles: {sum(counts.values())}", (14,55), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100,255,150), 1)
            cv2.putText(frame, "Q=quit  SPACE=pause", (14,78), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (160,160,160), 1)
            cv2.imshow("AAE4011 Vehicle Detection", frame)
            idx += 1
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        elif key == ord(' '):
            paused = not paused
    cv2.destroyAllWindows()
    print("Detection complete!")

if __name__ == '__main__':
    run_detection('/tmp/aae4011_frames')
