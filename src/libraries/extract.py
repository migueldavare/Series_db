from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
import os
from typing import List
from unittest.mock import patch
import pytest 

def generate_month_dates_as_strings(init_month: str) -> List[datetime.date]:
    """
    Generates a list of datetime.date objects for each day of a given month.

    Args:
        init_month (str): A string representing the year and month in 'YYYY-MM' format.

    Returns:
        List[datetime.date]: A list of datetime.date objects representing each day of the specified month.
                             Returns an empty list if the input month string is invalid.
    """
    init_date_str = init_month + '-01'
    list_days = []
    try:
        date_value = datetime.strptime(init_date_str, '%Y-%m-%d').date()
        next_month_date = (date_value + relativedelta(months=1))
        while date_value < next_month_date:
            list_days.append(date_value)
            date_value = date_value + relativedelta(days=1)
        return list_days
    except ValueError:
        print(f"Error: Invalid date string format '{init_date_str}'. Please use 'YYYY-MM'.")
        return []


def fetch_data_to_dataframe(url, method='GET'):
    """
    Makes a request to a specified URL and saves the JSON response data
    into a Pandas DataFrame.

    Args:
        url (str): The URL to make the request to.
        method (str, optional): HTTP method to use. Defaults to 'GET'.

    Returns:
        pandas.DataFrame or None: A Pandas DataFrame containing the data from the JSON response.
                                 Returns None if the request fails or the response is not valid JSON.
    """
    try:
        response = requests.request(method, url)
        response.raise_for_status()  

        try:
            data = response.json()
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])  
            else:
                print("Response JSON is not a list or a dictionary.")
                return None
            return df
        except ValueError:
            print("Response is not valid JSON.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    

def save_df_to_json_in_dir(df, filename, dir_path):
    """
    Saves a pandas DataFrame to a JSON file within a specified directory.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        filename (str): The name of the JSON file (e.g., 'data.json').
        dir_path (str): The path to the directory where the file should be saved.
                         This directory will be created if it doesn't exist.
    """
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, filename)

    try:
        df.to_json(file_path, orient='columns')  
        print(f"DataFrame successfully saved to: {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the DataFrame: {e}")


# unit test for generate_month_dates_as_strings
def test_valid_month():
    """Test with a valid month string."""
    result = generate_month_dates_as_strings("2025-03")
    assert len(result) == 31
    assert result[0] == date(2025, 3, 1)
    assert result[-1] == date(2025, 3, 31)

def test_another_valid_month():
    """Test with another valid month string (e.g., February of a non-leap year)."""
    result = generate_month_dates_as_strings("2025-02")
    assert len(result) == 28
    assert result[0] == date(2025, 2, 1)
    assert result[-1] == date(2025, 2, 28)

def test_leap_year_february():
    """Test with February of a leap year."""
    result = generate_month_dates_as_strings("2024-02")
    assert len(result) == 29
    assert result[0] == date(2024, 2, 1)
    assert result[-1] == date(2024, 2, 29)

def test_invalid_month_format():
    """Test with an invalid month string format."""
    result = generate_month_dates_as_strings("2025/03")
    assert result == []

def test_invalid_month_value():
    """Test with an invalid month value."""
    result = generate_month_dates_as_strings("2025-13")
    assert result == []

def test_invalid_year_format():
    """Test with an invalid year format."""
    result = generate_month_dates_as_strings("25-03")
    assert result == []

def test_empty_string():
    """Test with an empty string as input."""
    result = generate_month_dates_as_strings("")
    assert result == []

def test_partial_month_string():
    """Test with a partial month string."""
    result = generate_month_dates_as_strings("2025-")
    assert result == []

def test_invalid_month_format_output(capsys):
    """Test the printed output for an invalid month format."""
    generate_month_dates_as_strings("2025/03")
    captured = capsys.readouterr()
    assert "Error: Invalid date string format '2025/03-01'. Please use 'YYYY-MM'." in captured.out
    assert captured.err == ""


# unit test for fetch_data_to_dataframe

def test_fetch_data_success_list():
    """Test successful fetch with a JSON response as a list."""
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'[{"col1": "val1", "col2": 1}, {"col1": "val2", "col2": 2}]'
    mock_response.headers['Content-Type'] = 'application/json'

    with patch('requests.request', return_value=mock_response):
        df = fetch_data_to_dataframe("http://example.com/data")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2, 2)
        assert df.columns.tolist() == ["col1", "col2"]
        assert df["col1"].tolist() == ["val1", "val2"]
        assert df["col2"].tolist() == [1, 2]

def test_fetch_data_success_dict():
    """Test successful fetch with a JSON response as a dictionary."""
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"col1": "val1", "col2": 1}'
    mock_response.headers['Content-Type'] = 'application/json'

    with patch('requests.request', return_value=mock_response):
        df = fetch_data_to_dataframe("http://example.com/data")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (1, 2)
        assert df.columns.tolist() == ["col1", "col2"]
        assert df["col1"].tolist() == ["val1"]
        assert df["col2"].tolist() == [1]

def test_fetch_data_post_method_success():
    """Test successful fetch using the POST method."""
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'[{"col1": "val1"}]'
    mock_response.headers['Content-Type'] = 'application/json'

    with patch('requests.request', return_value=mock_response) as mock_request:
        df = fetch_data_to_dataframe("http://example.com/post_data", method='POST')
        assert isinstance(df, pd.DataFrame)
        assert mock_request.call_args[0][0] == 'POST'