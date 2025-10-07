import sys
sys.path.append(".")
sys.path.append("..")

from ultralytics import YOLO

# Initialize model (specifying both model architecture and pretrained weights)
model = YOLO(
    model='./cfg/models/12/yolo12-UAV.yaml',  # Model configuration file
    task='detect',                         # Task type: detection/segmentation/pose
)

# Training configuration (complete parameter mapping)  yolov12-based
results = model.train(
    # Required parameters
    data='./data/MOT-UAV.yaml',  # Dataset configuration file path 
    # For the Ultralytics framework, ​absolute paths must be used​ (for path )to avoid path resolution errors.
    epochs=50,  # Training duration
    batch=32,  # Batch size
    imgsz=1280,  # Input image size
    device='0,1,4,5',  # GPU device
    # Model saving
    lr0=0.00025,
    weight_decay=0.02,
    optimizer='AdamW',
    cos_lr=True,
    warmup_epochs=5,
    amp=True,
    project='exp',        # Output directory (default runs/detect)
)
