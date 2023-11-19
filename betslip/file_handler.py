# file_handler.py
import numpy as np
import os
from typing import Any

def find_project_root(current_path: str) -> str:
    """
    Traverse up the file system starting from the current_path to find the project root.

    Parameters:
    current_path (str): The starting path to begin the search.

    Returns:
    str: The path of the project root directory.
    """
    root_file = '.git'  # Replace with a filename or directory that is always at the root of your project
    while not os.path.exists(os.path.join(current_path, root_file)):
        new_path = os.path.dirname(current_path)
        if new_path == current_path:
            # Root of the file system reached without finding the root_file
            raise FileNotFoundError(f"Project root not found because {root_file} was not detected.")
        current_path = new_path
    return current_path

PROJECT_ROOT = find_project_root(os.path.dirname(__file__))
DEFAULT_FILE_PATH = os.path.join(PROJECT_ROOT, 'betslip', 'resource', 'data')

def save_to_npy(numpy_array: Any, file_name: str, file_path: str = DEFAULT_FILE_PATH) -> None:
    # Check if the file_path exists, create if it does not
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    # Construct the full path to the file
    full_path = os.path.join(file_path, file_name)

    # Save the array to the file
    np.save(full_path, numpy_array)

    print(f"Data saved successfully to {full_path}")