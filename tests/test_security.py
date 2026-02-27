import os
import shutil
from csv_exporter import CSVExporter

def test_sanitize_filename_prevents_path_traversal():
    """
    Test that _sanitize_filename correctly sanitizes malicious filenames.
    """
    # Test cases with path traversal and invalid characters
    test_cases = [
        ("../../etc/passwd", "passwd"),
        ("folder/file.csv", "file.csv"),
        ("my*cool?file.csv", "my_cool_file.csv"),
        ("..\\windows\\system32", "system32"),
    ]

    for malicious, expected in test_cases:
        sanitized = CSVExporter._sanitize_filename(malicious)
        assert sanitized == expected, f"Failed to sanitize '{malicious}'. Expected '{expected}', got '{sanitized}'"

def test_export_prevents_directory_escape(tmp_path):
    """
    Test that export method does not allow writing outside the intended directory.
    """
    # Setup
    base_dir = str(tmp_path)
    exporter = CSVExporter(base_path=base_dir)
    data = [{"col1": "val1"}]

    # Attempt to write to a file outside the directory
    malicious_filename = "../../evil_file"

    # Execute
    exporter.export(malicious_filename, data)

    # Verify
    # The sanitization should strip the path, so it should look for 'evil_file.csv'
    # inside the CanaData_MM-DD-YYYY folder in base_dir

    # Find the created directory (it will have today's date)
    created_dirs = [d for d in os.listdir(base_dir) if d.startswith("CanaData_")]
    assert len(created_dirs) == 1
    export_dir = os.path.join(base_dir, created_dirs[0])

    # Check if the sanitized file exists in the correct place
    expected_file = os.path.join(export_dir, "evil_file.csv")
    assert os.path.exists(expected_file), "Sanitized file should be created in the export directory"

    # Check that the file was NOT created outside
    evil_path_outside = os.path.join(tmp_path, "evil_file.csv")
    assert not os.path.exists(evil_path_outside), "File should not be created in the base directory"

    evil_path_root = os.path.join(tmp_path.parent, "evil_file.csv")
    assert not os.path.exists(evil_path_root), "File should not be created in the parent directory"
