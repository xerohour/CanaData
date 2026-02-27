import csv
import logging
import os
import re
from datetime import datetime
from os import path as ospath
from os import makedirs
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CSVExporter:
    """
    Handles export of data to CSV files with timestamped directories.
    """
    def __init__(self, base_path: str):
        self.base_path = base_path

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """
        Sanitize the filename to prevent path traversal and ensure valid file names.

        Args:
            filename (str): The original filename.

        Returns:
            str: The sanitized filename.
        """
        # Strip paths to prevent traversal (handles both / and \)
        safe_name = os.path.basename(filename.replace('\\', '/'))
        # Replace invalid characters with underscores, but allow dots
        safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', safe_name)
        return safe_name

    def export(self, filename: str, data: List[Dict[str, Any]]) -> None:
        """
        Export a list of dictionaries to a CSV file with timestamp.

        Creates a dated folder (CanaData_MM-DD-YYYY) relative to the base path
        and writes the data to a CSV file with headers from the first dictionary's keys.

        Args:
            filename (str): Base name for the CSV file (without extension)
            data (list): List of dictionaries with uniform keys

        Side Effects:
            - Creates CanaData_[date] folder if it doesn't exist
            - Writes CSV file to that folder
            - Prints success message with item count
        """
        # Sanitize filename
        safe_filename = self._sanitize_filename(filename)

        today = datetime.today().strftime('%m-%d-%Y')
        # Variable on where to save the file
        home_dir = f'{self.base_path}/CanaData_{today}'

        # Check if the folder exists
        if not ospath.exists(home_dir):
            # If not exist, create
            makedirs(home_dir)

        # Handle empty data case
        if not data:
            logger.warning(f"No data to export for {safe_filename}.csv")
            print(f'No data to export for {safe_filename}.csv')
            return

        # Create CSV file as outfile
        filepath = f'{home_dir}/{safe_filename}.csv'
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as outfile:
                # Setup csv writer with file
                output = csv.writer(outfile)

                # Row 1 Keys = first item in list's keys
                all_keys = list(data[0].keys())

                # Write row of keys
                output.writerow(all_keys)

                # Loop through the dataset
                for row in data:
                    # Write row of item's values
                    output.writerow(row.values())

                # Print visual notification of finished export & number of items seen
                print(f'Successfully exported ({str(len(data))} items) to CSV -> {safe_filename}.csv')
        except Exception as e:
            logger.error(f"Failed to export CSV {safe_filename}: {e}")
            raise e
