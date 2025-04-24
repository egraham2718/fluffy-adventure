from typing import Optional

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
MIN_YEAR, MAX_YEAR = 2000, 2_999

def input_amount() -> float:
    while True:
        entry = float(input(f"{'Amount:':20}"))
        if entry > 0:
            return entry
        else:
            print(f"Amount must be greater than zero.")


def input_int(entry_item: str, high: int, low: int = 1, fmt_width: int = 20) -> int:
    prompt = f"{entry_item.capitalize()} ({low}-{high}):"
    while True:
        entry = int(input(f"{prompt:{fmt_width}}"))
        if low <= entry <= high:
            return entry
        else:
            print(f"{entry_item.capitalize()} must be between {low} and {high}.")


def input_year() -> int:
    return input_int('year', MAX_YEAR, MIN_YEAR)


def input_month() -> int:
    return input_int("month", 12, fmt_width=20)


def input_day(year: int, month: int) -> int:
    max_day = cal_max_day(year, month)
    parameters = {"entry_item": "day", "high": max_day}
    # call input_int() using dictionary as keyword arguments
    return input_int(**parameters)


def input_date() -> str:
    while True:
        entry = input(f"{'Date (yyyy-mm-dd):':20}").strip()
        if len(entry) == 10 and entry[4] == '-' and entry[7] == '-' \
                and entry[:4].isdigit() and entry[5:7].isdigit() \
                and entry[8:].isdigit():
            yyyy, mm, dd = int(entry[:4]), int(entry[5:7]), int(entry[8:])
            if (1 <= mm <= 12) and (1 <= dd <= cal_max_day(yyyy, mm)):
                if MIN_YEAR <= yyyy <= MAX_YEAR:
                    return entry
                else:
                    print(f"Year of the date must be between {MIN_YEAR} and {MAX_YEAR}.")
            else:
                print(f"{entry} is not in a valid date format.")
        else:
            print(f"{entry} is not in a valid date format.")


def input_region_code() -> Optional[str]:
    while True:
        fmt = 20
        valid_codes = tuple(VALID_REGIONS.keys())
        prompt = f"{f'Region {valid_codes}:':{fmt}}"
        code = input(prompt)
        if valid_codes.count(code) == 1:
            return code
        else:
            print(f"Region must be one of the following: {valid_codes}.")


def from_input1() -> dict:
    amount = input_amount()
    year = input_year()
    month = input_month()
    day = input_day(year, month)
    sales_date = f"{year}-{str(month).zfill(2)}-{day:02}"
    region_code = input_region_code()
    return {"amount": amount,
            "sales_date": sales_date,
            "region": region_code,
            }


def from_input2() -> dict:
    amount = input_amount()
    sales_date = input_date()
    region_code = input_region_code()
    return {"amount": amount,
            "sales_date": sales_date,
            "region": region_code,
            }

def is_leap_year(year: int) -> bool:
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)


def cal_max_day(year: int, month: int) -> int:
    if is_leap_year(year) and month == 2:  # short-circuit
        return 29
    elif month == 2:
        return 28
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 31


def cal_quarter(month: int) -> int:
    if month in (1, 2, 3):
        quarter = 1
    elif month in (4, 5, 6):
        quarter = 2
    elif month in (7, 8, 9):
        quarter = 3
    elif month in (10, 11, 12):
        quarter = 4
    else:
        quarter = 0
    return quarter


def get_region_name(region_code: str) -> str:
    return VALID_REGIONS[region_code]


def is_valid_region(region_code: str) -> bool:
    return tuple(VALID_REGIONS.keys()).count(region_code) == 1


def has_bad_amount(data: dict) -> bool:
    return data["amount"] == "?"  # or data["amount"] < 0


def has_bad_date(data: dict) -> bool:
    return data["sales_date"] == "?"  # or not isinstance(self.sales_date, date)


def has_bad_data(data: dict) -> bool:
    return has_bad_amount(data) or has_bad_date(data)
