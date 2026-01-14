import json
import os
from datetime import datetime
from decimal import Decimal

import gspread
from google.oauth2.service_account import Credentials


def connecting():
    # Set the API scope for Google Sheets
    scope = ["https://www.googleapis.com/auth/spreadsheets"]

    # Load service account credentials from environment variable
    creds_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)

    # Authorize client
    client = gspread.authorize(creds)

    # Open workbook using key from environment variable
    workbook_id = os.getenv("WORKBOOK_ID")
    workbook = client.open_by_key(workbook_id)

    return workbook


def find_schedule(workbook):
    # Access the Schedule worksheet
    sheet = workbook.worksheet("Schedule")
    values_list = sheet.get_all_values("A2:N1001")

    upcoming_schedule = ""
    for row in values_list:
        if not row[6]:
            break
        name = row[1]
        location = row[4]
        format_string = "%a, %d-%m-%Y"
        date = datetime.strptime(row[6], format_string)
        service = row[7]
        price = row[8]
        status = row[12]

        # Include only future schedules that are not completed
        if date.date() >= datetime.today().date() and status != "Completed":
            upcoming_schedule += f"""<b>{name}</b>
                    📍 {location if location else "Not specify"}
                    📅 {date.strftime("%a, %d-%m-%Y") if date else "Not specify"}
                    ✨ {service if service else "Not specify"}
                    💵 {price if price else "Not specify"}

"""

    return upcoming_schedule or "No upcoming schedule"


def history_schedule(workbook, month_input):
    # Access the Schedule worksheet
    sheet = workbook.worksheet("Schedule")
    values_list = sheet.get_all_values("A2:N1001")

    history = ""
    num_of_client = 0
    total_money = 0
    for row in values_list:
        if not row[6]:
            break
        status = row[12]
        payment = row[11]
        format_string = "%a, %d-%m-%Y"
        date = datetime.strptime(row[6], format_string)
        month = row[5]
        service = row[7]
        total = row[10]
        name = row[1]
        location = row[4]

        # Include only completed services of the given month
        if status == "Completed" and month == month_input:
            num_of_client += 1
            total_money += float(total)
            history += f"""<b>{name}</b>
                    📍 {location if location else "Not specify"}
                    📅 {date.strftime("%a, %d-%m-%Y")}
                    ✨ {service if service else "Not specify"}
                    💵 {total if total else "Not specify"}
                    🧾 {payment if payment else "Not specify"}
                    ✅ {status}

"""

    return f"Num of clients: <b>{num_of_client}</b> | Total: <b>${total_money}</b>\n\n {history}" if num_of_client else "No history schedule"


def search_customer(workbook, customer_input):
    # Access the Customer Master worksheet
    sheet = workbook.worksheet("Customer Master")
    values_list = sheet.get_all_values("B5:F1000")

    for row in values_list:
        if not row[0]:
            break

        name = row[0]
        location = row[3]

        # Match customer name (case-insensitive)
        if customer_input.lower() in name.lower():
            return f"🙆‍♀️ <b>{name}</b>\n📍<b>{location}</b>"

    return "Not Found"


def calc_income(workbook, month_input):
    # Access the worksheet for the year 2026
    sheet = workbook.worksheet("2026")
    values_list = sheet.get_all_values("A5:H1000")

    temp_total_costs = 0
    temp_total_income = 0
    temp_total_profit = 0

    for row in values_list:
        if not row[6]:
            break

        total_cots = row[5]
        total_income = row[6]
        total_profit = row[7]
        format_string = "%a, %b-%d-%Y"
        date = datetime.strptime(row[1], format_string)
        month = int(datetime.strftime(date, "%m"))

        # Include only rows of the selected month or all months if 0
        if month_input != 0:
            month_input = int(month_input)
            if month_input == month:
                temp_total_costs += Decimal(total_cots)
                temp_total_income += Decimal(total_income)
                temp_total_profit += Decimal(total_profit)
        else:
            temp_total_profit += Decimal(total_profit)
            temp_total_costs += Decimal(total_cots)
            temp_total_income += Decimal(total_income)

    return f"""Total Income: ${temp_total_income}\nTotal Costs: ${temp_total_costs}\nTotal Profit: <b>${temp_total_profit}</b>
"""


def calc_total_customer(workbook):
    # Access the Customer Master worksheet
    sheet = workbook.worksheet("Customer Master")
    values_list = sheet.get_all_values("B2")

    total_customer = 0
    for row in values_list:
        total_customer += int(row[0])

    return total_customer