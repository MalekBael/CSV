# CSV to JSON Template Generator

This repository contains a Python script that generates JSON templates from CSV files. 

## Features

- Parse CSV files and read all rows.
- Output JSON files with structured definitions.

## File Structure

- `CSV.py`: The main Python script that performs the CSV to JSON conversion.
- `Definitions/`: Directory where generated JSON files are stored.
- `CSV/`: Directory containing the input CSV files.

## Usage

1. Place your CSV files in the `CSV/` directory.
2. Run the `CSV.py` script to generate JSON templates from the CSV files.
3. The generated JSON files will be saved in the `Definitions/` directory.

### Running the Script

To run the script, use the following command:

python CSV.py


## Work in Progress

This project is a work in progress. I am working on adding new features, improving existing functionality, and fixing bugs.

## Context

This tool helps extract data from CSV files, which are extracted from EXD files for the game Final Fantasy XIV. 
The generated JSON files emulate the structure of the Definition files from the Saint Coinach project. 
This tool can be handy when working with EXD files that Saint Coinach doesn't have definitions for, 
such as those from the base game A Realm Reborn.




