#!/usr/bin/env python3

import csv

with open('./web_archive_scraped_data.csv') as open_csv:
    csv_reader = csv.DictReader(open_csv)
    for row in csv_reader:
        print(row['call_number'])

