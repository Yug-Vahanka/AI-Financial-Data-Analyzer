#  IMPORT LIBRARIES 

import csv        # Used to read/write CSV files
import os         # Used for file and directory operations
import asyncio    # Used for async locking (to prevent concurrent writes)
# This avoids data corruption in concurrent API calls
csv_lock = asyncio.Lock()
#  CSV WRITE FUNCTION

async def write_to_csv(file_path, data, fieldnames):
    """
    Write data to CSV file safely using async lock.

    Args:
        file_path (str): Path to CSV file
        data (dict): Data to write as a row
        fieldnames (list): Column names for CSV
    """

    # Acquire lock to ensure only one write operation at a time
    async with csv_lock:

        #  CREATE DIRECTORY 

        os.makedirs(os.path.dirname(file_path), exist_ok=True)


        # CHECK FILE EXISTENCE

        file_exists = os.path.isfile(file_path)

        # Open file in append mode 
        with open(file_path, "a", newline="") as f:

            # Create CSV writer with given field names
            writer = csv.DictWriter(f, fieldnames=fieldnames)


            #  WRITE HEADER 

            if not file_exists:
                writer.writeheader()


            # WRITE DATA
            writer.writerow(data)