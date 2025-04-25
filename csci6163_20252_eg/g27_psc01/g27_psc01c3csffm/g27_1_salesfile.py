from functools import singledispatch
from pathlib import Path  # pathlib is preferred to os.path.join
import csv
import pickle

from g27_1_salesinput import cal_max_day

# files
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
FILEPATH = Path(__file__).parent.parent.parent / 'psc01_files'
ALL_SALES = 'all_sales.csv'
ALL_SALES_COPY = 'all_sales_copy.csv'
IMPORTED_FILES = 'imported_files.txt'

def is_valid_filename_format(filename: str) -> bool:
    if len(filename) == len(NAMING_CONVENTION) and \
            filename[:7] == NAMING_CONVENTION[:7] and \
            filename[8] == NAMING_CONVENTION[8] and \
            filename[13] == NAMING_CONVENTION[-6] and \
            filename[-4:] == NAMING_CONVENTION[-4:]:
        return True
    else:
        return False


def get_region_code_from_filename(sales_filename: str) -> str:
    return sales_filename[sales_filename.rfind('.') - 1]


def already_imported(filepath_name: Path) -> bool:
    """
    Return True if the given filename is in the IMPORTED_FILES.
    Otherwise, False.
    """
    # Complete code here
    try:
        with open(FILEPATH / IMPORTED_FILES) as file:
            files = [line.strip() for line in file.readlines()]
            return str(filepath_name) in files
    except FileNotFoundError:
        return False


def add_imported_file(filepath_name: Path) -> None:
    """Add the filepath_name into IMPORTED_FILES"""
    # Complete code here
    try:
        with open(FILEPATH / IMPORTED_FILES, "a") as file:
            file.write(f"{filepath_name}\n")
    except Exception as e:
        print(f"{type(e)} - The imported file could not be added.")

@singledispatch
def import_sales(filepath_name: Path, delimiter: str = ',') -> list:
    with open(filepath_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        filename = filepath_name.name
        region_code = filename[filename.rfind('.') - 1]
        imported_sales_list = []
        for amount_sales_date in reader:
            correct_data_types(amount_sales_date)
            amount, sales_date = amount_sales_date[0], amount_sales_date[1]
            data = {"amount": amount,
                    "sales_date": sales_date,
                    "region": region_code,
                    }
            imported_sales_list.append(data)
        return imported_sales_list  # within with statement

def correct_data_types(row) -> None:
    """
    Try to convert valid amount to float type
    and mark invalid amount or sales date as '?'
    """
    try:  # amount
        row[0] = float(row[0])  # convert to float
    except ValueError:
        row[0] = "?"  # Mark invalid amount as bad
    # date
    if len(row[1]) == 10 and row[1][4] == '-' and row[1][7] == '-' \
            and row[1][:4].isdigit() and row[1][5:7].isdigit() and row[1][8:10].isdigit():
        yyyy, mm, dd = int(row[1][:4]), int(row[1][5:7]), int(row[1][8:10])
        if not (1 <= mm <= 12) or not (1 <= dd <= cal_max_day(yyyy, mm)):
            row[1] = "?"  # Mark invalid date as bad
    else:
        row[1] = "?"  # Mark invalid date as bad

