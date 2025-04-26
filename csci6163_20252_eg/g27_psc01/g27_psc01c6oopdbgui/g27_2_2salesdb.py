from g27_1_1filetypes import FileType
from g27_1_1salestypes import Sales, Regions, Region
from typing import Optional
from pathlib import Path
from datetime import date
import sqlite3
from contextlib import closing

class SQLiteDBAccess:
    def __init__(self, db_name: str='', db_path: Path=None):        
        fname: str = db_name if db_name else 'sales_db.sqlite'
        fpath: Path = db_path if db_path else Path(__file__).parent.parent.parent / 'psc01_db'
        self._sqlite_sales_db = FileType(fname, fpath)
        self._valid_regions = Regions.from_dict()

    def __connect(self) -> Optional[sqlite3.Connection]:
    #"""Connect to the SQLite database and return the connection object."""
        conn = None
        try:
            # Establish a connection to the SQLite database
            if self._sqlite_sales_db:
                sqlite_db = self._sqlite_sales_db.dirpath / self._sqlite_sales_db.filename
                conn = sqlite3.connect(sqlite_db)
                print(f'Connection: {conn}')
                return conn
        except sqlite3.Error as e:
            print(f'{type(e)} Error connecting to the database: {self._sqlite_sales_db.filename}')
            if conn:
                conn.close()

    # ------------- Sales tbl---------------------
    # '''as of Python 3.12, sqlite3 no longer automatically converts datetime.date
    # objects into strings when passing them as query parameters.
    # You need to explicitly adapt or convert them to a supported format
    # (typically ISO 8601 string: "YYYY-MM-DD").
    # '''
    def retrieve_sales_by_date_region(self, sales_date: date, region_code: str) -> Optional[Sales]:
        conn = self.__connect()
        if conn:
            cursor = conn.cursor()
            query = '''SELECT ID, amount, salesDate, region
                        FROM sales
                        WHERE salesDate = ? AND region = ?'''
            cursor.execute(query,(sales_date.isoformat(), region_code))
            sales_record = cursor.fetchone()
            conn.close()

            if sales_record:
                return Sales(sales_record[1], # amount
                             sales_record[2], # sales_date
                             self._valid_regions.get_region_by_code(sales_record[3]), # region
                             sales_record[0] # id
                             )
            else:
                return None

    def update_sales(self, sales: Sales) -> None:
        conn = self.__connect()
        # cursor = conn.cursor()
        # query = '''UPDATE Sales 
        #            SET amount = ?, salesDate = ?, region = ?
        #            WHERE ID = ?'''
        # cursor.execute(query, (sales["amount"], 
        #                         sales["sales_date"].isoformat(), 
        #                         sales["region"].code, 
        #                         sales["ID"]))
        # conn.commit()
        # conn.close()
        
        with closing(conn.cursor()) as cur:
            query = '''UPDATE Sales 
                       SET amount = ?, salesDate = ?, region = ?
                       WHERE ID = ?'''
            cur.execute(query, (sales["amount"], 
                                sales["sales_date"].isoformat(), 
                                sales["region"].code, 
                                sales["ID"]))
            conn.commit()

    # ------------- Region table--------------
    def retrieve_regions(self) -> Optional[Regions]:
        conn = self.__connect()                         # Step 1: Create a connection
        if conn:
            cursor = conn.cursor()                      # Step 2: Create a cursor
            query = '''SELECT code, name FROM Region''' # Step 3: Create a query
            cursor.execute(query)                       # Step 4: Execute query
            records = cursor.fetchall()                 # Step 5: Fetch the result set
            conn.close()                                # Step 6: Release the resource
            if records:
                regions = Regions([], [])
                for record in records:
                    a_region = Region(record[0], record[1])
                    regions.add_region(a_region)
                return regions
        else:
            return None

def main():
    dbaccess = SQLiteDBAccess()
    results = dbaccess.retrieve_regions()
    for region in results:
        print(region)

if __name__ == '__main__':
    main()