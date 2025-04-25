from g27_2_salesmanager import (save_all_sales, initialize_content_of_files, import_all_sales, view_sales,
                                add_sales1, add_sales2, import_sales)

#-----------------Console Menu (Presentation) -----------------------
def display_title() -> None:
    print("SALES DATA IMPORTER\n")


def display_menu() -> None:
    cmd_format = "6"  # ^ center, < is the default for str.
    print("COMMAND MENU",
          f"{'view':{cmd_format}} - View all sales",
          f"{'add1':{cmd_format}} - Add sales by typing sales, year, month, day, and region",
          f"{'add2':{cmd_format}} - Add sales by typing sales, date (YYYY-MM-DD), and region",
          f"{'import':{cmd_format}} - Import sales from file",
          f"{'menu':{cmd_format}} - Show menu",
          f"{'exit':{cmd_format}} - Exit program", sep='\n', end='\n')


def execute_command() -> None:

    # initial content of the files all_sales.csv and imported_files.txt
    initialize_content_of_files()
    # initial content of sales_list
    sales_list = import_all_sales() # when application is started

    commands = {"import": import_sales,
                "add1": add_sales1,
                "add2": add_sales2,
                "view": view_sales,
                "menu": display_menu,
                }
    while True:
        action = input("\nPlease enter a command: ").strip().lower()
        if action == "exit":
            save_all_sales(sales_list)
            print("Saved sales records.")
            break
        if action == "import":
            commands[action](sales_list)
        elif action in ("add1", "add2"):
            commands[action](sales_list)
        elif action == "view":
            commands[action](sales_list)
        elif action == "menu":
            commands[action]()
        else:
            print("Invalid command. Please try again.\n")
            display_menu()
