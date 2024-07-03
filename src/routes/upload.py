from flask import Blueprint, jsonify, request
from google.cloud import storage
from src.services.service import files_to_dict, unzip_files, validate_files_exists
import os
import uuid

router = Blueprint("upload", __name__)

# Initialize GCS client
storage_client = storage.Client()

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

    zip_file = request.files['zipFile']
    csv_file = request.files['csvFile']

    # Check if both files have been selected
    if zip_file.filename == '' and csv_file.filename == '':
        return jsonify({"message": "No files selected. Both ZIP and CSV files are missing."}), 400
    elif zip_file.filename == '':
        return jsonify({"message": "No ZIP file selected."}), 400
    elif csv_file.filename == '':
        return jsonify({"message": "No CSV file selected."}), 400

    try:
        bucket_name = os.getenv('GCP_BUCKET_TEMPORARY') #bucket_name in Cloud Storage
        bucket = storage_client.bucket(bucket_name)

        # Generate unique filenames
        zip_filename = f"uploads/{uuid.uuid4()}-{zip_file.filename}"
        csv_filename = f"uploads/{uuid.uuid4()}-{csv_file.filename}"

        # Upload files to GCS
        blob = bucket.blob(zip_filename)
        blob.upload_from_file(zip_file)

        blob = bucket.blob(csv_filename)
        blob.upload_from_file(csv_file)

        return jsonify({"zipFile": zip_filename, "csvFile": csv_filename}), 200
    except Exception as error:
        return jsonify({"message": str(error)}), 500

@router.route("/compare-files", methods=["POST"])
def compare_files() -> jsonify:
    """
    This function handles the upload of a ZIP file and a CSV file,
    processes their contents, and validates if the files listed in the CSV
    are present in the ZIP.

    Args:
    - XX

    Returns:
    - XX

    Raises:
    - KeyError: If required files are not included in the request.
    """
    data = request.get_json()
    zip_filename = data.get('zipFile')
    csv_filename = data.get('csvFile')

    if not zip_filename or not csv_filename:
        return jsonify({"message": "Both ZIP and CSV file paths are required."}), 400

    try:
        bucket_name = os.getenv('GCP_BUCKET_TEMPORARY') #bucket_name in Cloud Storage
        bucket = storage_client.bucket(bucket_name)

        zip_blob = bucket.blob(zip_filename)
        csv_blob = bucket.blob(csv_filename)

        # Download files
        zip_file = zip_blob.download_as_bytes()
        csv_file = csv_blob.download_as_bytes()

        my_list = unzip_files(zip_file)
        my_dict = files_to_dict(csv_file)
        result = validate_files_exists(my_list, my_dict)
        
        return jsonify(result)
    except Exception as error:
        return jsonify({"message": str(error)}), 500
