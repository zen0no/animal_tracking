import os

DATA_FOLDER = os.getenv("DATA_FOLDER", "data") # temp files folder's name
SPICES_FILE = os.getenv("SPICES_FILE", "src/env/spices.json") # spices file
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
WEIGHTS = os.getenv("WEIGHTS", "../weights/yolo_v2.pt")
