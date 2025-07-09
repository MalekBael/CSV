# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
import re

def get_version(version_file_path):
    """
    Reads the version string from the given version file.
    Falls back to current date formatted version if an error occurs.
    """
    try:
        with open(version_file_path, 'r', encoding='utf-8') as vf:
            version = vf.readline().strip()
            if version:
                return version
    except Exception as e:
        print(f"Error reading version file: {e}")

    # Fallback to a date-based version format
    today = datetime.now()
    return f"{today.year}.{today.month:02d}.{today.day:02d}.0000.0000"

def combine_definition_files(input_dir, output_path, version_file_path):
    """
    Combines all JSON definition files into a single file with version information from the ffxivgame.ver file.
    """
    version = get_version(version_file_path)
    
    sheets = []
    
    # Iterate through all JSON files in the input directory
    for filename in sorted(os.listdir(input_dir)):
        if not filename.lower().endswith('.json'):
            continue
        
        file_path = os.path.join(input_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                definition = json.load(f)
                
            # Add the definition to our sheets list
            sheets.append(definition)
            print(f"Added {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Create the final structure
    result = {
        "version": version,
        "sheets": sheets
    }
    
    # Write the combined JSON file
    with open(output_path, 'w', encoding='utf-8') as outf:
        json.dump(result, outf, indent=2)
    
    print(f"\nSuccessfully created combined definition file: {output_path}")
    print(f"Combined {len(sheets)} sheet definitions")

if __name__ == '__main__':
    definitions_dir = os.path.join(os.getcwd(), "Definitions")  # Input directory with individual JSON files
    output_path = os.path.join(os.getcwd(), "Combined_definitions", "ex.json")  # Updated output path

    # Path to the ffxivgame.ver file
    version_file_path = r"C:\Program Files (x86)\SquareEnix\FINAL FANTASY XIV - A Realm Reborn\game\ffxivgame.ver"
    
    if not os.path.exists(definitions_dir):
        print(f"Error: Input directory '{definitions_dir}' not found.")
    else:
        combine_definition_files(definitions_dir, output_path, version_file_path)
