from typing import Optional, Self, Iterator, Union
from datetime import date
from dataclasses import dataclass

# use dataclass
@dataclass
class Region:
    _code: str = ""
    _name: str = ""

    # define property code
    @property
    def code(self):
        return self._code

    # define property name
    @property
    def name(self):
        return self._name


class Regions:
    def __init__(self, c_list: list, n_list: list) -> None:
        self._regions: list[Region] = [Region(c, n)
                                        for c, n in zip(c_list, n_list)]

    # define a classmethod from_dict(r_dict)
    @classmethod
    def from_dict(cls, r_dict: dict = None) -> Self:
        if r_dict is None:
            r_dict = {'w': 'West', 
                      'm': 'Mountain', 
                      'c': 'Central', 
                      'e': 'East'}
        return cls(list(r_dict.keys()), list(r_dict.values()))
        

    @property
    def regions(self) -> list:
        return self._regions

    # define a method so that you may use str(yourObj) or print(yourObj)
    def __str__(self) -> str:
        return str(self._regions)

    # define a method so that you may use a for loop
    def __iter__(self) -> Iterator[Region]:
        return iter(self._regions)

    def get_region_by_code(self, code: str) -> Optional[Region]:
        # Find and return the region object by code
        for region_obj in self._regions:
            if code == region_obj.code:
                return region_obj
        return None # Explicitly return None if the region is not found

    def get_region_code_list(self) -> list:
        return [region_obj.code for region_obj in self._regions]
    
    def is_valid_region_code(self, code: str) -> bool:
        for region_obj in self._regions:
            if code == region_obj.code:
                return True
        return False
    
    def add_region(self, region: Region=None) -> None:
        if region is not None:
            self._regions.append(region)


class Sales:
    DATE_FORMAT = "%Y-%m-%d" # Class constants
    MIN_YEAR, MAX_YEAR = 2000, 2_999

    def __init__(self,
            amount: float=0.0,
            sales_date: date=None,
            region: Region=None,
            id: int=0) -> None:
        
        self._salesdata = {"ID": id,
                            "amount": amount,
                            "sales_date": sales_date,
                            "region": region}

    def __str__(self) -> str:
        # '''override __str__() to customize what gets returned
        # when call print(), and str()
        # '''
        return (f"Sales(ID={self._salesdata["ID"]}, amount={self._salesdata["amount"]}, "
                f"date={self._salesdata["sales_date"]}, region={self._salesdata["region"]})")
    
    # Define a method so that we may use index operator
    # to update an element of a sales, such as sales[“amount”]=23.4
    def __setitem__(self, key: str, value: Optional[Union[int, date, float, Region, str]]) -> None:
        self._salesdata[key] = value

    # Define a method so that we may use index operator
    # to get a element value of a sales. Such as sales[“amount”]
    def __getitem__(self, key: str) -> Optional[Union[int, date, float, Region, str]]:
        return self._salesdata[key]

    @property
    def has_bad_amount(self) -> bool:
        return self._salesdata["amount"] == "?" # or self.amount <= 0

    @property
    def has_bad_date(self) -> bool:
        return self._salesdata["sales_date"] == "?" # or not isinstance(self.sales_date, date)

    @property
    def has_bad_data(self) -> bool:
        return self.has_bad_amount or self.has_bad_date

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

    @staticmethod
    def cal_max_day(year: int, month: int) -> int:
        if Sales.is_leap_year(year) and month == 2: # short-circuit
            return 29
        elif month == 2:
            return 28
        elif month in (4, 6, 9, 11):
            return 30
        else:
            return 31

    @staticmethod
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


class SalesList:
    def __init__(self):
        self._sales_list: list[Sales] = [] # Use a single underscore for protected attributes
        self._sales_id: int = 0

    @classmethod
    def from_list(cls, alist: list) -> Self:
        a_sales_list = cls()  # calls SalesList() constructor, __init__()
        for sales in alist:
            a_sales_list.add(sales)
        return a_sales_list

    def __iter__(self) -> Iterator[Sales]:
        return iter(self._sales_list)

    @property
    def count(self) -> int:
        # Return the number of items in the sales list
        return len(self._sales_list)

    @property
    def sales_id(self) -> int:
        return self._sales_id

    @sales_id.setter
    def sales_id(self, id: int) -> None:
        self._sales_id = id

    def __getitem__(self, index) -> Sales: # to use []
        return self._sales_list[index]

    def add(self, sales_obj: Sales) -> None:
        # Add a sales object to the list
        self._sales_list.append(sales_obj)
        self._sales_id += 1
        sales_obj['ID'] = self._sales_id

    def concat(self, other_list: list[Sales]=None) -> None:
        # Concatenate list of Sales (not SalesList)
        # into this one by iterating over it
        for sales in other_list:
            self.add(sales)

def main():
    pass

if __name__ == "__main__":
    main()