import csv

import yaml

with open("deductions_common.yaml") as file:
    test = yaml.safe_load(file)

with open("deductions.csv", "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    for key, value in test.items():
        writer.writerow([key, value])
