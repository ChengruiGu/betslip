# file_handler.py
import numpy as np
import os
from typing import Any
from .utils import DEFAULT_DATA_PATH
import pandas as pd
import logging

def save_to_npy(numpy_array: Any, file_name: str, file_path: str = DEFAULT_DATA_PATH) -> None:
    # Check if the file_path exists, create if it does not
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    file_name = f"{file_name}.npy" if not file_name.endswith(".npy") else file_name

    # Construct the full path to the file
    full_path = os.path.join(file_path, file_name)

    # Save the array to the file
    np.save(full_path, numpy_array)

    logging.info(f"Data saved successfully to {full_path}")

def load_from_npy(file_name: str, file_path: str = DEFAULT_DATA_PATH) -> Any:
    # Construct the full path to the file
    full_path = os.path.join(file_path, file_name)

    # Load the array from the file
    numpy_array = np.load(full_path, allow_pickle=True)

    return numpy_array

def save_to_pkl(data_frame: pd.DataFrame, file_name: str, file_path: str = DEFAULT_DATA_PATH) -> None:
    """
    Save a Pandas DataFrame to a pickle file.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame to save.
    file_name (str): The name of the file to which the DataFrame should be saved.
    file_path (str): The directory path where the file should be saved. Defaults to the default data path.

    Returns:
    None
    """
    # Check if the file_path exists, create if it does not
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    file_name = f"{file_name}.pkl" if not file_name.endswith(".pkl") else file_name

    # Construct the full path to the file
    full_path = os.path.join(file_path, file_name)

    # Save the DataFrame to the file
    data_frame.to_pickle(full_path)

    logging.info(f"DataFrame saved successfully to {full_path}")


def load_from_pkl(file_name: str, file_path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """
    Load a Pandas DataFrame from a pickle file.

    Parameters:
    file_name (str): The name of the file to load the DataFrame from.
    file_path (str): The directory path where the file is located. Defaults to the default data path.

    Returns:
    pd.DataFrame: The DataFrame loaded from the pickle file.
    """
    # Construct the full path to the file
    full_path = os.path.join(file_path, file_name)

    # Load the DataFrame from the file
    data_frame = pd.read_pickle(full_path)

    return data_frame


def save_to_csv(data_frame: pd.DataFrame, file_name: str, file_path: str = DEFAULT_DATA_PATH) -> None:
    """
    Save a Pandas DataFrame to a csv file.

    Parameters:
    data_frame (pd.DataFrame): The DataFrame to save.
    file_name (str): The name of the file to which the DataFrame should be saved.
    file_path (str): The directory path where the file should be saved. Defaults to the default data path.

    Returns:
    None
    """
    # Check if the file_path exists, create if it does not
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    file_name = f"{file_name}.csv" if not file_name.endswith(".csv") else file_name

    # Construct the full path to the file
    full_path = os.path.join(file_path, file_name)

    # Save the DataFrame to the file
    data_frame.to_csv(full_path)

    logging.info(f"DataFrame saved successfully to {full_path}")