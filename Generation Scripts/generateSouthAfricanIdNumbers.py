import subprocess
import sys
import time
import os
from datetime import datetime, timedelta
import ctypes

GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    try:
        import tqdm
        from tqdm import tqdm
    except ImportError:
        print("tqdm not found. Installing tqdm...")
        install('tqdm')
        try:
            import tqdm
            from tqdm import tqdm
        except ImportError:
            print("Failed to install tqdm. Please install it manually.")
            sys.exit(1)

    years = list(range(1960, 2001))

    def generate_dates_for_year(year):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
        dates = [(start_date + timedelta(days=i)).strftime("%y%m%d") for i in range((end_date - start_date).days)]
        return dates

    def generate_all_possibilities(year, file_name):
        date_prefixes = generate_dates_for_year(year)
        sequence_numbers = [f"{num:04d}" for num in range(10000)]
        citizenship_and_a = "08"
        
        total_iterations = len(date_prefixes) * len(sequence_numbers) * 10

        with open(file_name, 'w') as f, tqdm(total=total_iterations, desc=f"Generating ID numbers for {year}") as pbar:
            ids_to_write = []

            for date_prefix in date_prefixes:
                for seq_num in sequence_numbers:
                    id_number_without_checksum = f"{date_prefix}{seq_num}{citizenship_and_a}"
                    id_numbers = [f"{id_number_without_checksum}{checksum}" for checksum in range(10)]

                    ids_to_write.extend(id_numbers)
                    
                    if len(ids_to_write) > 1000:
                        f.write("\n".join(ids_to_write))
                        ids_to_write = []
                        pbar.update(1000)

            if ids_to_write:
                f.write("\n".join(ids_to_write))
                pbar.update(len(ids_to_write))

            pbar.update(total_iterations - pbar.n)

    overall_start_time = time.time()

    for year in years:
        file_name = f'sa_id_numbers_{year}.txt'
        file_start_time = time.time()
        generate_all_possibilities(year, file_name)
        file_end_time = time.time()

        os.system('cls' if os.name == 'nt' else 'clear')

        file_elapsed_time = file_end_time - file_start_time
        overall_elapsed_time = file_end_time - overall_start_time
        print(f"Generating ID numbers for {year}")
        print(f"\n{GREEN}Elapsed time for {year}: {file_elapsed_time:.2f} seconds{RESET}")
        print(f"{BLUE}Total elapsed time so far: {overall_elapsed_time:.2f} seconds{RESET}")

    overall_end_time = time.time()

    total_elapsed_time = overall_end_time - overall_start_time
    print(f"\n{BLUE}Total time elapsed: {total_elapsed_time:.2f} seconds{RESET}")
    print("Generated with 💚 by Code Dome (Pty) Ltd")

else:
    print("Attempting to run as administrator in PowerShell...")
    subprocess.run(['powershell', '-Command', 'Start-Process', sys.executable, f'"{__file__}"', '-Verb', 'runAs'])
    sys.exit(0)
