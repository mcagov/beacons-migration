from datetime import datetime

import csv
import os


def write_to_csv(results):
    directory = './migration_results/'
    os.makedirs(directory, exist_ok=True)

    filename = f"migration-report-{datetime.now().isoformat().replace(':', '-')}.csv"

    print(f'Writing results to: {directory} {filename}')

    with open(directory + filename, 'w', newline='') as csv_file:
        fieldnames = results[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow(result)
