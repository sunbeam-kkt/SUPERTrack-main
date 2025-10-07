import os
import random
import shutil

# 设置路径
base_dir = "/home/xcl/Track3-TrainDataset"
train_videos_dir = os.path.join(base_dir, "TrainVideos")
train_labels_dir = os.path.join(base_dir, "TrainLabels")

# 目标目录
target_root = "/home/xcl/Dist-Tracker-main/ultralytics/dataset_copy"
train_target_dir = os.path.join(target_root, "Yolo_train")
val_target_dir = os.path.join(target_root, "Yolo_val")

# 创建目标目录结构
for dataset_dir in [train_target_dir, val_target_dir]:
    os.makedirs(os.path.join(dataset_dir, "TrainVideos"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "TrainLabels"), exist_ok=True)

# 获取视频文件列表（不含后缀）
video_files = [f for f in os.listdir(train_videos_dir) if f.endswith(".mp4")]
base_names = [os.path.splitext(f)[0] for f in video_files]

# 筛选出同时存在标签文件的样本
valid_pairs = []
for name in base_names:
    video_path = os.path.join(train_videos_dir, name + ".mp4")
    label_path = os.path.join(train_labels_dir, name + ".txt")
    
    if os.path.exists(label_path):
        valid_pairs.append((name, video_path, label_path))
    else:
        print(f"警告：标签文件缺失 {name}.txt")

# 随机打乱并分割数据集
random.shuffle(valid_pairs)
split_idx = int(len(valid_pairs) * 0.8)
train_set = valid_pairs[:split_idx]
val_set = valid_pairs[split_idx:]

print(f"总样本数: {len(valid_pairs)}")
print(f"训练集大小: {len(train_set)}")
print(f"验证集大小: {len(val_set)}")

# 移动训练集文件
for name, video_src, label_src in train_set:
    # 移动视频文件
    video_dst = os.path.join(train_target_dir, "TrainVideos", name + ".mp4")
    shutil.move(video_src, video_dst)
    
    # 移动标签文件
    label_dst = os.path.join(train_target_dir, "TrainLabels", name + ".txt")
    shutil.move(label_src, label_dst)

# 移动验证集文件
for name, video_src, label_src in val_set:
    # 移动视频文件
    video_dst = os.path.join(val_target_dir, "TrainVideos", name + ".mp4")
    shutil.move(video_src, video_dst)
    
    # 移动标签文件
    label_dst = os.path.join(val_target_dir, "TrainLabels", name + ".txt")
    shutil.move(label_src, label_dst)

print("数据集分割完成！")
print(f"训练集已移动到: {train_target_dir}")
print(f"验证集已移动到: {val_target_dir}")