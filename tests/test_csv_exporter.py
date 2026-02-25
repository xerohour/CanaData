import os
import shutil
import csv
from datetime import datetime
from csv_exporter import CSVExporter

def test_csv_exporter_creates_directory_and_file():
    base_dir = "test_export_dir"
    exporter = CSVExporter(base_dir)
    filename = "test_file"
    data = [{"col1": "val1", "col2": "val2"}]

    try:
        exporter.export(filename, data)

        today = datetime.today().strftime('%m-%d-%Y')
        expected_dir = os.path.join(base_dir, f'CanaData_{today}')
        expected_file = os.path.join(expected_dir, f'{filename}.csv')

        assert os.path.exists(expected_dir)
        assert os.path.exists(expected_file)

        with open(expected_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            row = next(reader)

            assert headers == ["col1", "col2"]
            assert row == ["val1", "val2"]

    finally:
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

def test_csv_exporter_handles_empty_data():
    base_dir = "test_export_empty_dir"
    exporter = CSVExporter(base_dir)
    filename = "test_empty"
    data = []

    try:
        exporter.export(filename, data)

        today = datetime.today().strftime('%m-%d-%Y')
        expected_dir = os.path.join(base_dir, f'CanaData_{today}')
        expected_file = os.path.join(expected_dir, f'{filename}.csv')

        # Directory should be created (as per logic inside export: check exists -> create)
        # Wait, inside export:
        # home_dir = ...
        # if not exists(home_dir): mkdir(home_dir)
        # if not data: return
        # So yes, dir created, file not.

        assert os.path.exists(expected_dir)
        # File should NOT be created
        assert not os.path.exists(expected_file)

    finally:
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
