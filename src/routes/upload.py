from flask import Blueprint, jsonify, request
from src.services.service import files_to_dict, unzip_files, validate_files_exists

router = Blueprint("upload", __name__)

@router.route("/upload", methods=["POST"])
def upload_file() -> jsonify:
    """
    This function handles the upload of a ZIP file and a CSV file,
    processes their contents, and validates if the files listed in the CSV
    are present in the ZIP.

    Args:
    - None: The function directly uses Flask's request object to get files.

    Returns:
    - A JSON response containing the count and list of missing files, or an error message if files are missing.

    Raises:
    - KeyError: If required files are not included in the request.
    """

    # Check if both files are provided
    if 'zipFile' not in request.files and 'csvFile' not in request.files:
        return jsonify({"message": "No files selected. Both ZIP and CSV files are missing."}), 400
    elif 'zipFile' not in request.files:
        return jsonify({"message": "No ZIP file selected."}), 400
    elif 'csvFile' not in request.files:
        return jsonify({"message": "No CSV file selected."}), 400

    zip_folder = request.files['zipFile']
    csv_file_handler = request.files['csvFile']

    # Check if both files have been selected
    if zip_folder.filename == '' and csv_file_handler.filename == '':
        return jsonify({"message": "No files selected. Both ZIP and CSV files are missing."}), 400
    elif zip_folder.filename == '':
        return jsonify({"message": "No ZIP file selected."}), 400
    elif csv_file_handler.filename == '':
        return jsonify({"message": "No CSV file selected."}), 400

    try:
        my_list = unzip_files(zip_folder)
        my_dict = files_to_dict(csv_file_handler)
        result = validate_files_exists(my_list, my_dict)
        return jsonify(result)
    except Exception as error:
        return jsonify({"message": str(error)}), 500
