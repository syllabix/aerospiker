#!/usr/bin/env python3

import csv
from pathlib import Path

def generate_urls():
    # Get the directory of the current script
    script_dir = Path(__file__).parent
    
    # Input and output file paths
    input_file = script_dir / "base_data.csv"
    output_file = script_dir / "urls.txt"
    
    # Base URL template
    url_template = "http://localhost:8080/api/v1/retrieve/{set}/{key}"
    
    # Read CSV and generate URLs
    with open(input_file, 'r') as csv_file, open(output_file, 'w') as url_file:
        # Create CSV reader with header row
        csv_reader = csv.DictReader(csv_file)
        
        # Process each row and write URL
        for row in csv_reader:
            url = url_template.format(set=row['set'], key=row['key'])
            url_file.write(f"{url}\n")

if __name__ == "__main__":
    generate_urls()
    print("URLs have been generated in urls.txt") 