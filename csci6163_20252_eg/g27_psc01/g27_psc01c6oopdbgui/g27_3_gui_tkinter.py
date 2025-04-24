from g27_1_1salestypes import Sales
from g27_2_2salesdb import SQLiteDBAccess
from datetime import datetime
import tkinter as tk

# To override the basic Tk widgets, the import should follow the Tk import
from tkinter import ttk, messagebox


class SalesFrame(ttk.Frame):
    def __init__(self, parent):
        self._sqlite_dbaccess= SQLiteDBAccess() # used for db access

        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        self.sales_date_entry = None
        self.region_entry = None
        self.amount_entry = None
        self.id_entry = None
        self.getAmount_button = None
        self.clearField_button = None
        self.saveChanges_button = None
        # define string variable for text entry fields
        self.sales_date = tk.StringVar()
        self.region = tk.StringVar()
        self.amount = tk.StringVar()
        self.id = tk.StringVar()
        
        self.__init_components()

    def __init_components(self):
    # Display the grid of labels and text entry fields
        self.pack()

        ttk.Label(self, text="Enter date and region to get sales amount").grid(row=0, column=0, columnspan=4)

        ttk.Label(self, text="Date:").grid(row=1, column=0, sticky=tk.E)
        self.sales_date_entry = ttk.Entry(self, width=25, textvariable=self.sales_date)
        self.sales_date_entry.grid(row=1, column=1, columnspan=2)

        ttk.Label(self, text="Region:").grid(row=2, column=0, sticky=tk.E)
        self.region_entry = ttk.Entry(self, width=25, textvariable=self.region)
        self.region_entry.grid(row=2, column=1, columnspan=2)

        ttk.Label(self, text="Amount:").grid(row=3, column=0, sticky=tk.E)
        self.amount_entry = ttk.Entry(self, width=25, textvariable=self.amount,state=tk.DISABLED)
        self.amount_entry.grid(row=3, column=1, columnspan=2)

        ttk.Label(self, text="ID:").grid(row=4, column=0, sticky=tk.E)
        self.id_entry = ttk.Entry(self, width=25, textvariable=self.id, state="readonly")
        self.id_entry.grid(row=4, column=1, columnspan=2)

        # Create a frame to store the buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=5, columnspan=4, sticky=tk.E)

        # add button to button frame
        self.getAmount_button = ttk.Button(button_frame, text="Get Amount", command=self.__get_amount)
        self.getAmount_button.grid(row=0, column=0, padx=5)

        self.clearField_button = ttk.Button(button_frame, text="Clear Field", command=self.__clear_field)
        self.clearField_button.grid(row=0, column=1, padx=5)

        self.saveChanges_button = ttk.Button(button_frame, text="Save Changes", command=self.__save_changes, 
                                             state=tk.DISABLED)
        self.saveChanges_button.grid(row=0, column=2)

        ttk.Button(button_frame, text="Exit", 
                   command=self.parent.destroy).grid(row=0, column=3, padx=5)
        
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


    def __clear_field(self):
        self.id.set("")
        self.amount.set("")
        self.sales_date.set("")
        self.region.set("")
        self.sales_date_entry.config(state=tk.NORMAL)
        self.region_entry.config(state=tk.NORMAL)
        self.amount_entry.config(state=tk.DISABLED)
        self.getAmount_button.config(state=tk.NORMAL)
        self.clearField_button.config(state=tk.NORMAL)
        self.saveChanges_button.config(state=tk.DISABLED)

    #---------- DB Access--------------------------
    def __get_amount(self):
        v_sales_date = self.sales_date.get()
        v_region_code = self.region.get()
        if v_sales_date == ""or v_region_code == "":
            messagebox.showerror("Error", 
                                 "Please enter date and region to get sales amount")
        else:
            try:
                v_sales_date = datetime.strptime(v_sales_date,
                                                Sales.DATE_FORMAT).date()
                if v_sales_date.year < Sales.MIN_YEAR or v_sales_date > Sales.MAX_YEAR:
                    messagebox.showerror("Error", 
                                 "Invalid year.\n"
                                 f"A valid year is between {Sales.MIN_YEAR} and {Sales.MAX_YEAR}")
            except ValueError:
                messagebox.showerror("Error", 
                                 f"{v_sales_date} is not in a valid date format\n"
                                 f"yyyy-mm-dd")
            else:
                regions = self._sqlite_dbaccess.retrieve_regions() # Returns list of Region objects
                region_codes = tuple([region.code for region in regions])
                if v_region_code not in region_codes:
                    messagebox.showerror("Error", 
                                 f"{v_region_code} is not one of the following \n"
                                 f"region code: {region_codes}")
                else:
                    sales = self._sqlite_dbaccess.retrieve_sales_by_date_region(v_sales_date, v_region_code)
                    if sales is None:
                        self.id.set("")
                        self.amount.set("")
                        messagebox.showerror("Error", 
                                 "No sales found")
                    else:
                        self.amount.set(sales["amount"])
                        self.id.set(sales["ID"])
                        self.sales_date_entry.config(state=tk.DISABLED)
                        self.region_entry.config(state=tk.DISABLED)
                        self.amount_entry.config(state=tk.ACTIVE)
                        self.saveChanges_button.config(state=tk.NORMAL)

    def __save_changes(self):
        v_sales_date = self.sales_date.get()
        v_region_code = self.region.get()
        v_amount = self.amount.get()
        v_id = self.id.get()
        if v_id == '':
            messagebox.showerror("Error", 
                                 "No sales to save.")
        elif v_amount == "":
            messagebox.showerror("Error", 
                                 "Please enter amount to save sales amount.")
        else:
            v_id = int(v_id)
            v_amount = float(v_amount)
            v_sales_date = datetime.strptime(v_sales_date, Sales.DATE_FORMAT).date()

            regions = self._sqlite_dbaccess.retrieve_regions()
            region = regions.get_region_by_code(v_region_code)
            sales = Sales(v_amount, v_sales_date, region, v_id)
            
            self._sqlite_dbaccess.update_sales(sales)
            messagebox.showinfo("Success",
                                f"{str(sales)} is updated")
            self.__clear_field()

def main():
    root = tk.Tk()
    root.title("Edit Sales Amount")
    SalesFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()