import io
import zipfile


class TestUploadAPI:
    """Test suite for the 'upload' endpoint"""

    def test_upload_should_work(self, fake_client):
        """Funtion test to check the 'upload'
        endpoint with a successful POST request."""

        # ARRANGE: simulating CSV and ZIP files.
        example_csv = "filename;exists\nfile1.txt;1\nfile2.txt;1\n"
        example_zip = io.BytesIO()

        with zipfile.ZipFile(example_zip, "w") as zip_file:
            zip_file.writestr("file1.txt", "This is the content of file1.")
            zip_file.writestr("file2.txt", "This is the content of file2.")

        example_zip.seek(0)

        example_data = {
            "csvFile": (io.BytesIO(example_csv.encode("utf-8")), "test.csv"),
            "zipFile": (example_zip, "test.zip"),
        }

        # ACT: post request to the upload endpoint.
        response = fake_client.post(
            "/upload", content_type="multipart/form-data", data=example_data
        )

        # ASSERT
        assert response.status_code == 200  # noqa: PLR2004
        assert response.json["Count of missing files:"] == 0
        assert response.json["List of missing files:"] == []

    def test_upload_should_detect_missing_files(self, fake_client):
        """Funtion test to check the 'upload'
        endpoint with a successful POST request."""

        # ARRANGE: simulating CSV and ZIP files.
        example_csv = "filename;exists\nfile1.txt;1\nfile2.txt;1\n"
        example_zip = io.BytesIO()

        with zipfile.ZipFile(example_zip, "w") as zip_file:
            zip_file.writestr("file1.txt", "This is the content of file1.")

        example_zip.seek(0)

        example_data = {
            "csvFile": (io.BytesIO(example_csv.encode("utf-8")), "test.csv"),
            "zipFile": (example_zip, "test.zip"),
        }

        # ACT: post request to the upload endpoint.
        response = fake_client.post(
            "/upload", content_type="multipart/form-data", data=example_data
        )

        # ASSERT
        assert response.status_code == 200  # noqa: PLR2004
        assert response.json["Count of missing files:"] == 1
        assert response.json["List of missing files:"] == ["file2.txt"]
        