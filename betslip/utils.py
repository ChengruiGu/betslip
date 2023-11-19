from datetime import datetime
import numpy as np


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