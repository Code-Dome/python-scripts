import sys
import subprocess
import time
from tqdm import tqdm

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
YELLOW = '\033[93m'

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_tqdm():
    try:
        import tqdm
    except ImportError:
        print("tqdm not found. Installing tqdm...")
        install('tqdm')
        import tqdm

check_and_install_tqdm()

def find_id_in_file(id_number, file_name):
    try:
        with open(file_name, 'r') as file:
            print(f"{YELLOW}Loading file and preparing search...{RESET}")
            time.sleep(1)  

            total_lines = sum(1 for _ in file)
            file.seek(0)

            with tqdm(total=total_lines, desc="Searching for ID", unit="line", ncols=100) as pbar:
                for i, line in enumerate(file):
                    if line.strip() == id_number:
                        return True, i + 1
                    pbar.update(1)
    except FileNotFoundError:
        print(f"{RED}File {file_name} not found.{RESET}")
        return False, None
    return False, None

def extract_year_from_id(id_number):
    year_prefix = id_number[:2]
    year = 1900 + int(year_prefix)
    return year

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <id_number>")
        sys.exit(1)

    id_number = sys.argv[1]

    if len(id_number) != 13:
        print(f"{RED}ID number must be exactly 13 characters long.{RESET}")
        sys.exit(1)
    
    year = extract_year_from_id(id_number)
    file_name = f'sa_id_numbers_{year}.txt'
    
    found, line_number = find_id_in_file(id_number, file_name)
    
    if found:
        print(f"{GREEN}ID number {id_number} found in {file_name} on line {line_number}.{RESET}")
    else:
        print(f"{RED}ID number {id_number} not found in {file_name}.{RESET}")

if __name__ == "__main__":
    main()

print('')
print("Generated with 💚 by Code Dome (Pty) Ltd")
