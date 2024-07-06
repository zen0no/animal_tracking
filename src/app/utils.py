from PIL import Image
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


def visualisation(path, boxes, labels):
    img = Image.open(path)
    sections = []
    for label, (x1, y1, x2, y2) in zip(labels, boxes):
        x1 *= img.size[0]
        y1 *= img.size[1]
        x2 *= img.size[0]
        y2 *= img.size[1]
        sections.append((map(int, (x1, y1, x2, y2)), label))

    return (img, sections)
