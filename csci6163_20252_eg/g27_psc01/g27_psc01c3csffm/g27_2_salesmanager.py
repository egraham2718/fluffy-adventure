from pathlib import Path  # pathlib is preferred to os.path.join

from g27_1_salesinput import (get_region_name, has_bad_amount, has_bad_data, has_bad_date, is_valid_region,
                              from_input1, from_input2, cal_quarter)
from g27_1_salesfile import (already_imported, is_valid_filename_format, add_imported_file, correct_data_types,
                             get_region_code_from_filename, import_sales)

import csv

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
# files
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
FILEPATH = Path(__file__).parent.parent.parent / 'psc01_files'
ALL_SALES = 'all_sales.csv'
ALL_SALES_COPY = 'all_sales_copy.csv'
IMPORTED_FILES = 'imported_files.txt'


def view_sales(sales_list: list) -> bool:
    bad_data_flag = False
    if len(sales_list) == 0:  # sales_list could be [] or None
        print("No sales to view.")
    else: # not empty
        col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15  # column width
        total_w = col1_w + col2_w + col3_w + col4_w + col5_w
        print(f"{' ':{col1_w}}"
              f"{'Date':{col2_w}}"
              f"{'Quarter':{col3_w}}"
              f"{'Region':{col4_w}}"
              f"{'Amount':>{col5_w}}")
        print(horizontal_line := f"{'-' * total_w}")
        total = 0.0

        for idx, sales in enumerate(sales_list, start=1):
            if has_bad_data(sales):
                bad_data_flag = True
                num = f"{idx}.*"   # add period and asterisk
            else:
                num = f"{idx}."    # add period only

            amount = sales["amount"]
            if not has_bad_amount(sales):
                total += amount

            sales_date = sales["sales_date"]
            if has_bad_date(sales):
                bad_data_flag = True
                month = 0
            else:
                month = int(sales_date.split("-")[1])

            region = get_region_name(sales["region"])
            quarter = f"{cal_quarter(month)}"
            print(f"{num:<{col1_w}}"
                  f"{sales_date:{col2_w}}"
                  f"{quarter:<{col3_w}}"
                  f"{region:{col4_w}}"
                  f"{amount:>{col5_w}}")

        print(horizontal_line)
        print(f"{'TOTAL':{col1_w}}"
              f"{' ':{col2_w + col3_w + col4_w}}"
              f"{total:>{col5_w}}\n")
    return bad_data_flag


def add_sales1(sales_list: list) -> None:
    """
     Get the sales data from_input1() which
     asks user to enter sales amount and date by calling following functions
       - input_amount,
       - input_year, input_month, input_day
       - input_region_code
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    # get the sales data from_input1()
    sales_list.append(data := from_input1())
    print(f"Sales for {data["sales_date"]} is added.")


def add_sales2(sales_list: list) -> None:
    """
     Get the sales data from_input2() which
     asks user to enter sales amount and date by calling following functions
       - input_amount,
       - input_date,
       - input_region_code
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    # get the sales data from_input2()
    sales_list.append(data := from_input2())
    print(f"Sales for {data["sales_date"]} is added.")


def import_all_sales() -> list:
    """
    Read each row of sales data from the file ALL_SALES into a dictionary
    data = {"amount": amount,
            "sales_date": sales_date,
            "region": region_code}
    Return a list of dictionaries.
    """
    # complete the code
    
    with (open(FILEPATH / ALL_SALES, newline='') as csvfile):
        reader = csv.reader(csvfile)
        sales_list = []
        for line in reader:
            if len(line) > 0:
                # Only write one line of code here to get amount, sales_date and region_code  
                # correct_data_types(amount_sales_date)
                # amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                correct_data_types(line)
                amount, sales_date, region_code = line
                data = {"amount": amount,
                        "sales_date": sales_date,
                        "region": region_code,
                        }
                sales_list.append(data)
        return sales_list  # within with statement


@import_sales.register
def _(sales_list: list)-> None:
    filename = input("Enter name of file to import: ")
    filepath_name = FILEPATH / filename
    if not is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of {NAMING_CONVENTION}.")
    elif not is_valid_region(get_region_code_from_filename(filename)):
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(VALID_REGIONS.keys())}.")
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "")
        print(f"File '{filename}' has already been imported.")
    else:
        imported_sales_list = import_sales(filepath_name)
        if imported_sales_list is None:
            print(f"Fail to import sales from '{filename}'.")
        else:
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\n"
                      "Please correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:
                    sales_list.extend(imported_sales_list)
                    print("Imported sales added to list.")
                    add_imported_file(filepath_name)


def save_all_sales(sales_list, delimiter: str=',') -> None:
    """
    Convert each sales data dictionary in the sales_list into a list
    Save the converted sales list which now is a list of lists into the file ALL_SALES.
    """
    # convert the list of dictionaries to a list of lists, using comprehension
    list_object = [[value for value in dict_obj.values()] for dict_obj in sales_list]
    
    # Save the converted sales list which now is a list of lists into the file ALL_SALES.
    with open(FILEPATH / ALL_SALES, 'w', newline='') as sales_file:
        csv_w = csv.writer(sales_file)

        csv_w.writerows(list_object)

def initialize_content_of_files(delimiter: str=',') -> None:
    """
    Make sure the SALES_ALL contains the same content of SALES_ALL_COPY.
    Make sure the IMPORTED_FILES is empty
    """
    with open(FILEPATH / ALL_SALES, 'w', newline='') as sales_file, open(FILEPATH / ALL_SALES_COPY, 'r') as sales_copy_file:
        csv_w = csv.writer(sales_file)

        csv_r = csv.reader(sales_copy_file)
        for line in csv_r:
            csv_w.writerow(line)

    with open(FILEPATH / IMPORTED_FILES, 'w') as imp_file:
        pass
