from datetime import datetime

import csv
import os

def write_to_csv(results):
  directory = "./migration_results/"
  os.makedirs(directory, exist_ok=True)

  filename = datetime.now().isoformat() + ".csv"

  print("Writing results to: " + directory + filename)

  with open(directory + filename, 'w', newline='') as csvfile:
    fieldnames = results[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()

    for result in results:
        writer.writerow(result)