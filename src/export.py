"""
Attendance Excel export utilities
"""

from datetime import datetime, timezone, timedelta
import openpyxl
from src.gdrive import download_file, upload_file
from src.telegram import send_message

# Load template from google drive
TEMPLATE = download_file()
wb = openpyxl.load_workbook(TEMPLATE)
ws = wb["Active Members"]

# Row and column numbers of interest in excel template
DATE_ROW = 8
LEFT_DATE_LIMIT = 5
RIGHT_DATE_LIMIT = 14
NAME_START_ROW = 10
NAME_COL = 2
MAX_NAME_ROW = 170


def get_target_column(export_date):
    """
    Get target column in excel sheet for given export date.

    Args:
        export_date (int): Day to be exported.

    Returns:
        int: Target column number if found, else None.
    """
    for col in range(LEFT_DATE_LIMIT, RIGHT_DATE_LIMIT):
        if int(ws.cell(row=DATE_ROW, column=col).value) == export_date:
            print(f"Target column for date {export_date} is column {col}.")
            return col

    print(f"Date {export_date} not found in the sheet!")
    return None


def zero_missing_members(col_no):
    """
    Fill empty cells in column with 0.

    Args:
        col_no (in): Target column.
    """
    for row in range(NAME_START_ROW + 1, MAX_NAME_ROW):
        cell_value = ws.cell(row=row, column=col_no).value

        if not cell_value or int(cell_value) != 1:
            ws.cell(row=row, column=col_no, value=0)


def insert_entries(export_date, entries):
    """
    Insert name entries into Excel sheet.

    Args:
        export_date (int): Day to be exported.
        entries (list): List of Member entries.
    """
    target_date = export_date
    target_column = get_target_column(target_date)

    if not target_column:
        print(f"Target column {target_column} not found in Attendance sheet.")
        return

    attendance_names = list(map(lambda x: x["name"], entries))
    duplicate_names = []
    missing_names = []

    for name in attendance_names:
        matching_rows = []

        for row in range(NAME_START_ROW + 1, ws.max_row + 1):
            cell_value = ws.cell(row=row, column=NAME_COL).value
            if isinstance(cell_value, str) and name.lower() in cell_value.lower():
                matching_rows.append(row)

        if len(matching_rows) == 1:
            row_to_update = matching_rows[0]
            ws.cell(row=row_to_update, column=target_column, value=1)
            print(f"Marked {name} as present on {target_date} (Row {row_to_update}).")
        elif len(matching_rows) > 1:
            # Duplicate name entry
            # TODO: possible enhancement of feature using member status
            print(f"Skipping {name}, Found multiple matches: {matching_rows}")
            duplicate_names.append(name)
        else:
            # Name not found
            print(f"{name} not found.")
            missing_names.append(name)

    zero_missing_members(target_column)

    # Send telegram status message
    sgt = timezone(timedelta(hours=8))
    month = datetime.now(sgt).month
    day_month = f"{export_date}/{month}"
    send_message(day_month, duplicates=duplicate_names, missing=missing_names)

    # Save and upload excel sheet to google drive
    wb.save(TEMPLATE)
    wb.close()
    upload_file()
