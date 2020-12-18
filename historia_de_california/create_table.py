#!/usr/bin/env python3
'''
creates a table named `bancroft_documents` inside of an sqlite3 db
that shows where specific volumes and/or documents could be found
pertaining to the historia de california archives
'''

import csv
import re
import sqlite3


def roman_to_decimal(value: str) -> int:
    result = 0
    roman = {
        'M': 1000,
        'CM': 900,
        'D': 500,
        'CD': 400,
        'C': 100,
        'XC': 90,
        'L': 50,
        'XL': 40,
        'X': 10,
        'IX': 9,
        'V': 5,
        'IV': 4,
        'I': 1,
    }
    # relies upon dict being ordered (official feature as of python 3.7)
    for numeral in roman:
        while value.upper().startswith(numeral):
            result += roman.get(numeral)
            value = value[len(numeral):]
    return result


conn = sqlite3.connect('historia_de_california.db')
cur = conn.cursor()

#cur.execute('''
#    DROP TABLE IF EXISTS bancroft_documents
#''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS bancroft_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        volume INTEGER,
        document_no INTEGER,
        document_name TEXT,
        call_number TEXT,
        document_url TEXT
    )
''')

with open('./web_archive_scraped_data.csv') as open_csv:
    csv_reader = csv.DictReader(open_csv)
    for row in csv_reader:
        # regex that finds Tomo with roman numeral (range), or a Docs. decimal value (range)
        document_ranges = re.findall(r'(Tomo[s]* [LXVI\-]+|Docs. [0-9\-]+)',
                                     row['volume'])

        # edge case for entries without values for document_no or volume
        if len(document_ranges) == 0:
            cur.execute(
                '''
                INSERT INTO bancroft_documents (document_name, call_number, document_url)
                VALUES (?, ?, ?)
                ''', (row['document_name'], row['call_number'],
                      row['document_url']))

        for document_range in document_ranges:
            document_range = document_range.split()[1].split('-')
            try:
                document_range = [int(value) for value in document_range]
                field = 'document_no'
            except ValueError:
                field = 'volume'
                document_range = [
                    roman_to_decimal(roman) for roman in document_range
                ]

            if len(document_range) == 1:
                document_range.append(document_range[0])

            for document in range(document_range[0], document_range[1] + 1):
                cur.execute(
                    f'''
                    INSERT INTO bancroft_documents ({field}, document_name, call_number, document_url)
                    VALUES (?, ?, ?, ?)
                    ''', (document, row['document_name'], row['call_number'],
                          row['document_url']))

conn.commit()
conn.close()
