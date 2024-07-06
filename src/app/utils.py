import json
import uuid
import zipfile
import os
import shutil
from typing import List
from env.env import DATA_FOLDER


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
        extracted_files = [os.path.join(DATA_FOLDER, unique_name, name) for name in zip_ref.namelist() if not name.endswith('/')]
    
    return extracted_files


def clear_temp_data():
    """Clears all data in the temporary folder.

    Raises:
        OSError: If there are issues with deleting the temporary folder contents.
    """
    if os.path.exists(DATA_FOLDER):
        shutil.rmtree(DATA_FOLDER)
        os.makedirs(DATA_FOLDER)


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


def get_file_info(files: list[str]) -> dict:
    """Returns a dictionary with the number of files in each trap folder.

    Args:
        files (List[str]): A list of file paths.

    Returns:
        Dict[str, Dict[str, int]]: A dictionary with the count of files in each folder.
    """
    trap_counts = {}

    for file in files:
        # Extract the folder name (e.g., '1', '2')
        parts = file.split(os.sep)
        if len(parts) > 2:
            trap_folder = parts[-2]
            if trap_folder.isdigit():
                if trap_folder not in trap_counts:
                    trap_counts[trap_folder] = 0
                # Increment count for the trap folder
                if not file.endswith('/'):
                    trap_counts[trap_folder] += 1

    return {"фотоловушки": trap_counts}
