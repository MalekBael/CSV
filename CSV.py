# -*- coding: utf-8 -*-
import os
import csv
import json
from collections import OrderedDict

def parse_csv(csv_path):
    """Reads all rows from the CSV file."""
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    return rows

def generate_template_from_csv(csv_rows, sheet_name, csv_folder):
    """
    Generates a JSON template from the CSV header rows.
    
    Processing:
      - Skip column 0.
      - Determine the default column as the first non-link field.
      - Then, for each column (from 1 onward), if the CSV column index is >= default_pos,
        assign a new sequential index (starting at 1) and output keys in the order:
            "index", "name", and (if applicable) "converter"
      - If the field name matches the pattern "Data[...]", it is replaced with "Data".
    """
    if len(csv_rows) < 2:
        print("CSV does not have enough rows to generate a template.")
        return None

    header_keys = csv_rows[0]
    header_names = csv_rows[1]

    # First pass: determine default column position (default_pos) and value.
    default_pos = None
    default_column = None
    for i in range(1, len(header_keys)):
        field = header_names[i].strip() if i < len(header_names) else ""
        if not field:
            field = header_keys[i].strip()
        # Transform "Data[...]" fields to "Data"
        if field.startswith("Data[") and field.endswith("]"):
            field = "Data"
            
        link_csv_path = os.path.join(csv_folder, field + ".csv")
        # First non-link field becomes default.
        if default_pos is None and not os.path.exists(link_csv_path):
            default_pos = i
            default_column = field

    if default_pos is None:
        default_pos = 1
        default_column = header_names[1].strip() if len(header_names) > 1 else ""

    definitions = []
    seq_index = 0  # sequential index for columns at or after default_pos

    # Second pass: create definitions.
    for i in range(1, len(header_keys)):
        field = header_names[i].strip() if i < len(header_names) else ""
        if not field:
            field = header_keys[i].strip()
        if field.startswith("Data[") and field.endswith("]"):
            field = "Data"

        link_csv_path = os.path.join(csv_folder, field + ".csv")
        is_link = os.path.exists(link_csv_path)
        
        if i >= default_pos:
            seq_index += 1
            entry = OrderedDict()
            entry["index"] = seq_index
            entry["name"] = field
            if is_link:
                entry["converter"] = {
                    "type": "link",
                    "target": field
                }
        else:
            entry = {"name": field}
            if is_link:
                entry["converter"] = {
                    "type": "link",
                    "target": field
                }
        definitions.append(entry)
    
    template = {
        "sheet": sheet_name,
        "defaultColumn": default_column,
        "definitions": definitions
    }
    return template

def main(root_dir):
    csv_folder = os.path.join(root_dir, "CSV")
    output_folder = os.path.join(root_dir, "Definitions")
    os.makedirs(output_folder, exist_ok=True)

    for csv_filename in os.listdir(csv_folder):
        if not csv_filename.lower().endswith(".csv"):
            continue
        csv_path = os.path.join(csv_folder, csv_filename)
        csv_rows = parse_csv(csv_path)
        
        base_name = os.path.splitext(csv_filename)[0]
        sheet_name = base_name.capitalize()
        
        generated_template = generate_template_from_csv(csv_rows, sheet_name, csv_folder)
        if generated_template is None:
            continue

        output_filename = base_name + ".json"
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "w", encoding="utf-8") as outf:
            json.dump(generated_template, outf, indent=2)
        
        print(f"Generated JSON file: {output_path}")

if __name__ == '__main__':
    cwd = os.getcwd()  # Expects folders: CVS and Definitions
    main(cwd)
