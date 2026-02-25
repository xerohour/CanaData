import csv
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CSVExporter:
    """
    Handles export of data to CSV files in timestamped directories.
    """
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def export(self, filename: str, data: List[Dict[str, Any]]) -> None:
        """
        Export a list of dictionaries to a CSV file.

        Args:
            filename (str): Base name for the CSV file (without extension)
            data (list): List of dictionaries with uniform keys
        """
        today = datetime.today().strftime('%m-%d-%Y')
        # Variable on where to save the file
        # Replicating original logic: f'{path[0]}/CanaData_{today}'
        # Here base_dir is path[0]
        home_dir = os.path.join(self.base_dir, f'CanaData_{today}')

        # Check if the folder exists
        if not os.path.exists(home_dir):
            # If not exist, create
            os.makedirs(home_dir)

        # Handle empty data case
        if not data:
            logger.warning(f"No data to export for {filename}.csv")
            print(f'No data to export for {filename}.csv')
            return

        # Create CSV file as outfile
        filepath = os.path.join(home_dir, f'{filename}.csv')

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
        print(f'Successfully exported ({str(len(data))} items) to CSV -> {filename}.csv')
        logger.info(f"Successfully exported {len(data)} items to {filepath}")
