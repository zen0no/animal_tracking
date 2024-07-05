import zipfile
import os
import shutil
from typing import List
from env.env import TEMP_FOLDER

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
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    extracted_files = []

    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(TEMP_FOLDER)
        extracted_files = [os.path.join(TEMP_FOLDER, name) for name in zip_ref.namelist()]
    
    return extracted_files


def clear_temp_data():
    """Clears all data in the temporary folder.

    Raises:
        OSError: If there are issues with deleting the temporary folder contents.
    """
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
        os.makedirs(TEMP_FOLDER)
