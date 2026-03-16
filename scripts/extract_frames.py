import os, argparse, cv2
import numpy as np
from rosbags.rosbag1 import Reader
from rosbags.typesys import Stores, get_typestore

def extract_frames(bag_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Opening: {bag_path}")
    typestore = get_typestore(Stores.ROS1_NOETIC)
    count = 0
    with Reader(bag_path) as reader:
        print("Topics found:")
        for topic, msgtype in reader.topics.items():
            print(f"  {topic} ({msgtype.msgtype})")
        for conn in reader.connections:
            if 'image' in conn.topic.lower() or 'camera' in conn.topic.lower():
                print(f"\nExtracting from: {conn.topic}")
                for rawdata in reader.messages(connections=[conn]):
                    _, timestamp, data = rawdata
                    try:
                        msg = typestore.deserialize_ros1(data, conn.msgtype)
                        arr = np.frombuffer(msg.data, dtype=np.uint8)
                        if 'compressed' in conn.topic.lower():
                            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                        else:
                            h, w = msg.height, msg.width
                            img = arr.reshape((h, w, 3))
                            if msg.encoding == 'rgb8':
                                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                        if img is not None:
                            cv2.imwrite(f"{output_dir}/frame_{count:05d}.jpg", img)
                            count += 1
                            if count % 50 == 0:
                                print(f"  Extracted {count} frames...")
                    except Exception as e:
                        continue
    print(f"\nDone! Extracted {count} frames to {output_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bag', required=True)
    parser.add_argument('--output', default='/tmp/aae4011_frames')
    args = parser.parse_args()
    extract_frames(args.bag, args.output)
