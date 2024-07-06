import json
import pandas as pd
from ultralytics import YOLO
from PIL.ExifTags import TAGS

from env.env import SPICES_FILE, WEIGHTS


# Загрузка модели YOLOv8
MODEL = YOLO(WEIGHTS)

def predict(model, images):
    classes = []
    bboxes = []
    idx = []

    results = model.predict(images)
    for i, r in enumerate(results):
        bb = r.boxes
        xyxyn = list(bb.xyxyn.detach().cpu().numpy())
        bb_class = list(bb.cls.detach().cpu().numpy())
        _idx = [i] * bb.cls.shape[0]
        
        classes.append([model.names[int(cls_)] for cls_ in bb_class])
        bboxes.append(xyxyn)
        idx.append(_idx)

    return {
        'id': idx, 'bbox': bboxes, 'class_predict': classes
    }


def get_spices(filepath: str = SPICES_FILE) -> str:
    """
    Reads a JSON file containing spices and returns them as a list of strings.

    Args:
        filepath (str): The path to the JSON file. Defaults to SPICES_FILE.

    Returns:
        list: A list of spices.

    Raises:
        FileNotFoundError: If the file specified by filepath is not found.
        json.JSONDecodeError: If the file contains invalid JSON.
        KeyError: If the key 'spices' is not found in the JSON file.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
        if "spices" not in data:
            raise KeyError("The key 'spices' is not found in the JSON file.")
        return data["spices"]


def get_exif_data(image):
    """Получить метаданные EXIF из изображения"""
    exif_data = image._getexif()
    if exif_data is not None:
        exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
        return exif
    return {}

def get_date_from_exif(image):
    """Получить дату из метаданных EXIF"""
    exif_data = get_exif_data(image)
    date = exif_data.get('DateTimeOriginal') or exif_data.get('DateTime')
    if date:
        return pd.to_datetime(date, format='%Y:%m:%d %H:%M:%S')
    return pd.NaT


def get_model_config(model=MODEL):
    """
    Returns a JSON-formatted string representing the configuration for a YOLO model.

    This function generates a dictionary with configuration parameters for a YOLO model and converts it to a formatted JSON string.

    Returns:
        str: A JSON-formatted string containing the YOLO model configuration.
    """
    config = {
        "input_size": model.input_size if hasattr(model, 'input_size') else "unknown",
        "stride": model.stride if hasattr(model, 'stride') else "unknown",
        "conf_thres": model.conf if hasattr(model, 'conf') else "unknown",
        "iou_thres": model.iou if hasattr(model, 'iou') else "unknown",
        "device": str(model.device) if hasattr(model, 'device') else "unknown",
    }
    return json.dumps(config, indent=4)
