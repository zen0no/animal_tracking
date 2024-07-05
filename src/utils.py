import json
import uuid
import zipfile
import os
import shutil
from typing import List
from env.env import SPICES_FILE, DATA_FOLDER


def extract_files(file) -> List[str]:
    """Extracts zip file to a temporary folder and returns a list of extracted file paths.

    Args:
        file (file-like object): A file-like object representing the zip file to be extracted.

    Returns:
        List[str]: A list of paths to the extracted files.

    Raises:
        zipfile.BadZipFile: If the file is not a zip file or it is corrupted.
        OSError: If there are issues with file extraction or creating the temporary folder.
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    unique_name = uuid.uuid4().hex
    os.makedirs(os.path.join(DATA_FOLDER, unique_name))

    extracted_files = []
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(DATA_FOLDER, unique_name))
        extracted_files = [os.path.join(DATA_FOLDER, unique_name, name) for name in zip_ref.namelist()]
    
    return extracted_files


def clear_temp_data():
    """Clears all data in the temporary folder.

    Raises:
        OSError: If there are issues with deleting the temporary folder contents.
    """
    if os.path.exists(DATA_FOLDER):
        shutil.rmtree(DATA_FOLDER)
        os.makedirs(DATA_FOLDER)


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


def get_model_config():
    """
    Returns a JSON-formatted string representing the configuration for a YOLO model.

    This function generates a dictionary with configuration parameters for a YOLO model and converts it to a formatted JSON string.

    Returns:
        str: A JSON-formatted string containing the YOLO model configuration.
    """
    yolo_config = {
        "model": "yolov5",
        "confidence_threshold": 0.5,
        "nms_threshold": 0.4,
        "input_size": (640, 640)
    }
    return json.dumps(yolo_config, indent=4)
