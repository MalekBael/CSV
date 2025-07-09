import os
import csv
import json
import yaml

def parse_csv_fieldnames(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 1st row: indices
        # Find the first non-empty, non-comment row (field names)
        while True:
            row = next(reader)
            if any(cell.strip() for cell in row) and not row[0].startswith('#'):
                fieldnames = row
                break
    return fieldnames[1:]  # Skip rowid


def get_link_targets(csv_folder):
    return {os.path.splitext(f)[0] for f in os.listdir(csv_folder) if f.lower().endswith('.csv')}

def build_definitions(fieldnames, link_targets):
    definitions = []
    for idx, name in enumerate(fieldnames):
        if idx == 0:
            continue  # Skip index 0, as it's the defaultColumn
        definition = {
            "index": idx,
            "name": name if name else str(idx)
        }
        # Add link converter for common link fields
        if "PlaceName" in name:
            definition["converter"] = {"type": "link", "target": "PlaceName"}
        elif name == "Map":
            definition["converter"] = {"type": "link", "target": "Map"}
        elif name == "Mount":
            definition["converter"] = {"type": "link", "target": "Mount"}
        elif name == "BGM":
            definition["converter"] = {"type": "link", "target": "BGM"}
        elif name == "TerritoryIntendedUse":
            definition["converter"] = {"type": "link", "target": "TerritoryIntendedUse"}
        # Add icon converter for icon fields
        if "Icon" in name or name == "LoadingImage" or name.endswith("Icon"):
            definition["converter"] = {"type": "icon"}
        definitions.append(definition)
    return definitions

def generate_json_for_sheet(csv_path, csv_folder):
    fieldnames = parse_csv_fieldnames(csv_path)
    link_targets = get_link_targets(csv_folder)
    definitions = build_definitions(fieldnames, link_targets)
    default_column = fieldnames[0] if fieldnames else ""
    sheet_name = os.path.splitext(os.path.basename(csv_path))[0]
    return {
        "sheet": sheet_name,
        "defaultColumn": default_column,
        "definitions": definitions
    }

def fill_names_from_yaml(json_path, yaml_path):
    if not os.path.exists(yaml_path):
        return  # No YAML mapping, skip
    with open(yaml_path, encoding='utf-8') as f:
        yml = yaml.safe_load(f)
    fields = yml['fields']
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    # Update definitions with YAML names and converters
    for i, definition in enumerate(data['definitions']):
        field_idx = definition['index']
        if field_idx < len(fields):
            field = fields[field_idx]
            if isinstance(field, dict):
                definition['name'] = field.get('name', str(field_idx))
                if 'type' in field and field['type'] == 'icon':
                    definition['converter'] = {"type": "icon"}
                elif 'type' in field and field['type'] == 'link':
                    targets = field.get('targets', [])
                    if targets:
                        definition['converter'] = {"type": "link", "target": targets[0]}
            else:
                definition['name'] = str(field)
    # Set defaultColumn from YAML
    if 'displayField' in yml:
        data['defaultColumn'] = yml['displayField']
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated {json_path} with YAML names.")

def batch_fill_names_from_yaml(yaml_folder, json_folder):
    for yaml_file in os.listdir(yaml_folder):
        if not yaml_file.lower().endswith('.yaml'):
            continue
        base = os.path.splitext(yaml_file)[0]
        yaml_path = os.path.join(yaml_folder, yaml_file)
        json_path = os.path.join(json_folder, base + ".json")
        if os.path.exists(json_path):
            fill_names_from_yaml(json_path, yaml_path)
        else:
            print(f"Warning: {json_path} does not exist for {yaml_path}")

def main():
    csv_folder = "CSV"
    output_folder = "Definitions"
    yaml_folder = "YAML"
    os.makedirs(output_folder, exist_ok=True)
    # Generate JSON from all CSVs
    for csv_file in os.listdir(csv_folder):
        if not csv_file.lower().endswith('.csv'):
            continue
        csv_path = os.path.join(csv_folder, csv_file)
        output = generate_json_for_sheet(csv_path, csv_folder)
        json_path = os.path.join(output_folder, os.path.splitext(csv_file)[0] + ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Generated {json_path}")
    # Post-process all YAMLs for their respective JSONs
    batch_fill_names_from_yaml(yaml_folder, output_folder)

if __name__ == "__main__":
    main()
