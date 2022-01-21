import csv

import yaml

with open("deductions_common.yaml") as file:
    all_deductions = yaml.safe_load(file)

with open("deductions.csv", "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    for key, value in all_deductions.items():
        writer.writerow([key, value])
