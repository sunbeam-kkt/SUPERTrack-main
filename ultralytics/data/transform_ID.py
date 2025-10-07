# 用于修改标签文件类别的脚本
import os

def convert_labels(label_dir):
    for file in os.listdir(label_dir):
        if file.endswith('.txt'):
            filepath = os.path.join(label_dir, file)
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            for line in lines:
                parts = line.split()
                if parts[0] == '1':
                    parts[0] = '0'  # 将类别1改为0
                    new_lines.append(' '.join(parts) + '\n')
                else:
                    new_lines.append(line)
            
            with open(filepath, 'w') as f:
                f.writelines(new_lines)

# 在分割数据集前调用此函数
convert_labels("/home/xcl/Dist-Tracker-main/ultralytics/dataset/Yolo_val/labels")