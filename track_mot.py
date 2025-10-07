import sys
sys.path.append(".")
sys.path.append("..")

import os
from ultralytics import YOLO
import csv

# Define model path
model = YOLO("best.pt")

# Input and output paths
input_folder = "./dataset/Videos"
output_folder = "./processed_results/"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get all video files in input folder
video_extensions = ('.mp4')  # Supported formats
video_files = [f for f in os.listdir(input_folder) if f.endswith(video_extensions)]

for video_file in video_files:
    video_path = os.path.join(input_folder, video_file)
    print(f"Processing: {video_file}")
    
    # 创建MOT格式的结果保存路径
    mot_output_path = os.path.join(output_folder, f"{os.path.splitext(video_file)[0]}_MOT.txt")
    
    # 打开文件准备写入MOT格式结果
    with open(mot_output_path, 'w', newline='') as mot_file:
        writer = csv.writer(mot_file, delimiter=',')
        
        # 运行跟踪并逐帧处理
        results = model.track(
            source=video_path,
            stream=True,  # 启用流模式避免内存溢出
            save_conf=True,
            save_txt=False,
            imgsz=1280,
            conf=0.25,  # 建议设置合理阈值
            device=6,
            show_labels=True,
            show_conf=False,
            save=True,
            line_width=1,
            save_frames=True,
            project=output_folder,
            name=os.path.splitext(video_file)[0]
        )
        
        for frame_idx, r in enumerate(results, start=1):
            if r.boxes.id is None:
                continue  # 跳过无检测的帧
                
            # 获取当前帧的跟踪数据
            track_ids = r.boxes.id.cpu().numpy().astype(int)
            confs = r.boxes.conf.cpu().numpy()
            boxes_xyxy = r.boxes.xyxy.cpu().numpy()
            
            # 写入MOT格式: <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, -1, -1, -1
            for track_id, conf, box in zip(track_ids, confs, boxes_xyxy):
                x1, y1, x2, y2 = box
                width = x2 - x1
                height = y2 - y1
                writer.writerow([
                    frame_idx,
                    track_id,
                    x1, y1, width, height,
                    conf,
                    -1, -1, -1  # MOT格式要求的占位符
                ])
    
    print(f"Saved MOT results to: {mot_output_path}")
    print(f"Finished processing: {video_file}")
    
print("All videos processed successfully!")