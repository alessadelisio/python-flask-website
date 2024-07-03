import csv
import zipfile
from io import BytesIO

def files_to_dict(csv_data: bytes) -> dict:
    """
    This function converts a CSV file data to a dictionary.

    Args:
    - csv_file (FileStorage): The CSV file stored in a
    FileStorage object.

    Returns:
    - csv_dict (dict): A dictionary containing data from
    the CSV file.

    Raises:
    - Exception: If an error occurs.
    """

    csv_dict = {}

    try:
        csv_stream = csv_data.decode("utf-8")
        csv_reader = csv.reader(csv_stream.splitlines(), delimiter=";")

        next(csv_reader) # Skip the first row of the CSV document.

    except Exception as error:
        raise Exception("Error: csv_file could not be read.") from error

    for row in csv_reader:
        # Assume column 1 is the key and column 2 is the value.
        key = row[0]
        value = row[1]

        # Add the key-values ​​to the dictionary  . 
        csv_dict[key] = value

    return csv_dict


def unzip_files(zip_data: bytes) -> list:
    """
    This function processes the content of a ZIP object.

    Args:
    - zip_file (FileStorage): The ZIP file stored in a
    FileStorage object.

    Returns:
    - zip_list_files (list): A list of all the files
    within the ZIP object.

    Raises:
    - Exception: If an error occurs.
    """

    zip_list_files = []

    try:
        with zipfile.ZipFile(BytesIO(zip_data), mode="r") as my_zip:
            zip_list_files = my_zip.namelist()

    except Exception as error:
        raise Exception("Error: `zip_file` could not be read.") from error

    return zip_list_files

def validate_files_exists(zip_list: list, csv_dict: dict) -> dict:
    """
    This function validates the information in
    a CVS file againts the content of a folder.

    Args:
    - zip_list (list): A list of files within a ZIP
    object.
    - csv_dict (dict): A dictionary containing data from
    the CSV file.

    Returns:
    - response (dict): A dictionary containing the
    number of missing files and a list of them.
    """

    missing_files = []

    for file in csv_dict:
        if file not in zip_list:
            missing_files.append(file)

    response = {
        "Count of missing files:": len(missing_files),
        "List of missing files:": missing_files,
    }

    return response
