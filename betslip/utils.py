from datetime import datetime
import numpy as np
import os
import pandas as pd


def convert_datetime_to_timestamp(date_string, date_format = "%Y-%m-%d %H:%M:%S"):
    """
    Convert a date string to a Unix timestamp (in milliseconds)
    
    :param date_string: The date string to convert.
    :param date_format: The format of the date string.
    :return: Unix timestamp in milliseconds.
    """
    # Parse the date string into a datetime object
    dt = datetime.strptime(date_string, date_format)
    
    # Convert the datetime object to a Unix timestamp (in seconds)
    timestamp_seconds = int(dt.timestamp())
    
    # Convert seconds to milliseconds
    timestamp_milliseconds = timestamp_seconds * 1000
    
    return timestamp_milliseconds

# Function to convert timestamps to human-readable format and create a NumPy array
def convert_to_numpy(data_dict):
    data_points = data_dict['data']['item']
    np_data = np.array(data_points)
    human_readable_dates = [datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S") for ts in np_data[:, 0].astype(np.int64)]
    np_data[:, 0] = human_readable_dates
    return np_data

def convert_to_dataframe(data_dict) -> pd.DataFrame:
    # Extract column names and data points
    column_names = data_dict['data']['column']
    data_points = data_dict['data']['item']
    
    # Create a DataFrame from the data points
    df = pd.DataFrame(data_points, columns=column_names)
    
    # Convert the timestamp to a human-readable date if the first column is the timestamp
    # Assuming the first column contains the timestamp
    if 'timestamp' in column_names:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    return df

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
DEFAULT_DATA_PATH = os.path.join(PROJECT_ROOT, 'betslip', 'resource', 'data')
DEFAULT_CONFIG_PATH = os.path.join(PROJECT_ROOT, 'betslip', 'resource', 'sample_config.json')

PERIODS = {'day', 'week', 'month', 'quarter', 'year', '120m', '60m', '30m', '15m', '5m', '1m'}