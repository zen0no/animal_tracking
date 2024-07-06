import json

from env.env import SPICES_FILE


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
