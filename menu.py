# -*- coding: utf-8 -*-
import os
import sys
import subprocess

def clear_screen():
    """Clear the console screen based on operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Print the main menu."""
    print("\n" + "=" * 50)
    print("FFXIV CSV PROCESSING TOOL".center(50))
    print("=" * 50)
    print("\n1. Generate JSON definitions from CSV files")
    print("2. Combine JSON definitions into a single file")
    print("3. Exit program")
    print("\n" + "=" * 50)

def run_csv_processor():
    """Run the CSV processing script."""
    print("\nRunning CSV Processor...")
    try:
        subprocess.run([sys.executable, "CSV.py"], check=True)
        print("\nCSV processing completed successfully.")
    except subprocess.CalledProcessError:
        print("\nAn error occurred while running the CSV processor.")
    
    input("\nPress Enter to return to the main menu...")

def run_combine_definitions():
    """Run the definitions combiner script."""
    print("\nRunning Definition Combiner...")
    
    # Ensure the output directory exists
    output_dir = os.path.join(os.getcwd(), "notes")
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if the Definitions folder exists
    if not os.path.exists("Definitions"):
        print(f"Error: Definitions directory not found.")
        print("Please run option 1 first to generate the definition files.")
    else:
        try:
            subprocess.run([sys.executable, "combine_definitions.py"], check=True)
            print("\nDefinition combining completed successfully.")
        except subprocess.CalledProcessError:
            print("\nAn error occurred while running the definition combiner.")
    
    input("\nPress Enter to return to the main menu...")

def main():
    """Main program loop."""
    while True:
        clear_screen()
        print_menu()
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            run_csv_processor()
        elif choice == '2':
            run_combine_definitions()
        elif choice == '3':
            print("\nExiting program. Goodbye!")
            sys.exit(0)
        else:
            input("\nInvalid choice. Press Enter to try again...")

if __name__ == "__main__":
    main()
