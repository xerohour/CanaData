import os
import shutil
import pytest
from CanaData import CanaData
from datetime import datetime
from sys import path

def test_path_traversal_prevention():
    cana = CanaData()

    # malicious filename trying to write outside the intended directory
    # Intended: ./CanaData_MM-DD-YYYY/filename.csv
    # Attack: ../traversal_test

    malicious_filename = "../traversal_test"
    data = [{"col1": "val1", "col2": "val2"}]

    today = datetime.today().strftime('%m-%d-%Y')
    expected_dir = f'{path[0]}/CanaData_{today}'

    # Clean up before test
    if os.path.exists(expected_dir):
        shutil.rmtree(expected_dir)

    leaked_file = f"{path[0]}/traversal_test.csv"
    if os.path.exists(leaked_file):
        os.remove(leaked_file)

    # Attempt export
    cana.csv_maker(malicious_filename, data)

    # 1. Verify file was NOT created outside directory
    assert not os.path.exists(leaked_file), "Path traversal vulnerability: File created outside target directory!"

    # 2. Verify file WAS created with sanitized name inside directory
    # The sanitizer replaces invalid chars (dots, slashes) with underscores
    # so "../traversal_test" becomes "___traversal_test" (roughly, depending on exact logic)
    # The current logic is: os.path.basename("../traversal_test") -> "traversal_test"
    # then re.sub -> "traversal_test" (if no dots). Wait, "traversal_test" has no dots.
    # If the input was just "../traversal_test", basename is "traversal_test".

    # Let's check what the sanitized name should be
    # basename("../traversal_test") -> "traversal_test"
    # re.sub(..., "traversal_test") -> "traversal_test"

    sanitized_path = f"{expected_dir}/traversal_test.csv"
    assert os.path.exists(sanitized_path), f"Sanitized file not found at {sanitized_path}"

    # Clean up
    if os.path.exists(expected_dir):
        shutil.rmtree(expected_dir)

def test_sanitize_filename_logic():
    cana = CanaData()

    # Test simple case
    assert cana._sanitize_filename("clean_file") == "clean_file"

    # Test path components
    assert cana._sanitize_filename("../parent_dir") == "parent_dir"
    assert cana._sanitize_filename("/absolute/path") == "path"

    # Test special characters
    # "my.file" -> "my_file" because '.' is not in [a-zA-Z0-9_-]
    assert cana._sanitize_filename("my.file") == "my_file"

    # Test mixed
    # "../bad.dir/evil;file" -> basename: "evil;file" -> regex: "evil_file"
    assert cana._sanitize_filename("../bad.dir/evil;file") == "evil_file"
