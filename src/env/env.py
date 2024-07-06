import os

DATA_FOLDER = os.getenv("DATA_FOLDER", "data") # temp files folder's name
SPICES_FILE = os.getenv("SPICES_FILE", "src/env/spices.json") # spices file
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
YOLO_PATH = os.getenv("YOLO_PATH", "weights/yolo.yolo.pt")
