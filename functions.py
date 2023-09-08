import csv
from datetime import *
from datetime import date
import argparse
from rich.console import Console
from rich.table import Table
import json

current_day_file = "date.json"


def buy_product(product_name, buy_price, expiration_date):
    buy_date = get_current_day(current_day_file).strftime("%Y-%m-%d")
    id = str(get_next_purchace_id())
    data = [id, product_name, buy_date, buy_price, expiration_date]
    field_names = ["id", "product_name", "buy_date", "buy_price", "expiration_date"]

    try:
        with open("bought.csv", "a") as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Adds fieldnames if file is empty
                writer.writerow(field_names)
            writer.writerow(data)
            print(f"OK: Bought {product_name} for €{buy_price:.2f}.")

    except Exception as e:
        print(f"An error occurred: {e}")


def sell_product(product_name, sell_price):
    sell_date = get_current_day(current_day_file).strftime("%Y-%m-%d")
    field_names = [
        "id",
        "product_name",
        "buy_date",
        "sell_date",
        "buy_price",
        "sell_price",
        "expiration_date",
    ]
    sold_products = set()

    try:
        with open("bought.csv", "r+") as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                bought_data = line.split(",")
                if product_name in line and product_name not in sold_products:
                    data = [
                        bought_data[0],
                        product_name,
                        bought_data[2],
                        sell_date,
                        bought_data[3],
                        sell_price,
                        bought_data[4].strip(),
                    ]
                    with open("sold.csv", "a") as sold_file:
                        writer = csv.writer(sold_file)
                        if sold_file.tell() == 0:  # Adds fieldnames if file is empty
                            writer.writerow(field_names)
                        writer.writerow(data)
                        print(f"OK: Sold {product_name} for €{sell_price:.2f}")
                    sold_products.add(product_name)
                else:
                    file.write(line)
            file.truncate()

        if product_name not in sold_products:
            print(f"ERROR: {product_name} not in stock.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Report functions
console = Console()

# Inventory
inventory_table = Table(show_header=True, header_style="bold magenta")
inventory_table.add_column("Product")
inventory_table.add_column("Count")
inventory_table.add_column("Buy Price")
inventory_table.add_column("Expiration Date")


def report_inventory(date):
    inventory_list = []
    reference_date = date

    with open("bought.csv", "r") as bought_file, open("sold.csv", "r") as sold_file:
        bought_lines = bought_file.readlines()
        sold_lines = sold_file.readlines()

        for line in bought_lines:
            bought_data = line.strip().split(",")
            if len(bought_data) < 6:
                continue
            if bought_data[0] == "id":
                continue  # skip when we iterate over the fieldnames

            # If inventory is empty AND the date we are checking is after buy date > append
            if (
                len(inventory_list) == 0
                and reference_date
                >= datetime.strptime(bought_data[2], "%Y-%m-%d").date()
            ):  # if inventory_list is empty appends the item
                inventory_list.append(
                    [bought_data[1], 1, bought_data[3], bought_data[4]]
                )
                continue

            # checks if the item matches [product_name, buy_price and expiration_date], if True then adds 1 to the existing count
            found = False
            for item in inventory_list:
                if (
                    bought_data[1] == item[0]
                    and bought_data[3] == item[2]
                    and bought_data[4] == item[3]
                ):
                    item[1] += 1
                    found = True
                    break

            # if not found AND the date we are checking is after buy date > append
            if (
                not found
                and reference_date
                >= datetime.strptime(bought_data[2], "%Y-%m-%d").date()
            ):
                inventory_list.append(
                    [bought_data[1], 1, bought_data[3], bought_data[4]]
                )

        # inventory logic for sold.csv file
        for line in sold_lines:
            sold_data = line.strip().split(",")
            if len(sold_data) < 6:
                continue
            if sold_data[0] == "id":
                continue  # skip when we iterate over the fieldnames
            # If inventory is empty AND the date we are checking is after buy date AND before sell date > append
            if (
                len(inventory_list) == 0
                and reference_date >= datetime.strptime(sold_data[2], "%Y-%m-%d").date()
                and reference_date < datetime.strptime(sold_data[3], "%Y-%m-%d").date()
            ):
                inventory_list.append([sold_data[1], 1, sold_data[4], sold_data[-1]])

            # checks if the items matches AND the reference date is after buy date AND before sell date, if True then adds 1 to the existing count
            found = False
            for item in inventory_list:
                if (
                    sold_data[1] == item[0]
                    and sold_data[4] == item[2]
                    and sold_data[-1] == item[3]
                    and reference_date
                    >= datetime.strptime(sold_data[2], "%Y-%m-%d").date()
                    and reference_date
                    < datetime.strptime(sold_data[3], "%Y-%m-%d").date()
                ):
                    item[1] += 1
                    found = True
                    break

            # if not found AND the date we are checking is after buy date > append
            if (
                not found
                and reference_date >= datetime.strptime(sold_data[2], "%Y-%m-%d").date()
                and reference_date < datetime.strptime(sold_data[3], "%Y-%m-%d").date()
            ):
                inventory_list.append([sold_data[1], 1, sold_data[4], sold_data[-1]])

    for item in inventory_list:
        inventory_table.add_row(item[0], str(item[1]), item[2], item[3])
    console.print(inventory_table)


# Revenue
def report_revenue(date):
    revenue = 0

    with open("sold.csv", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.split(",")
            if len(data) < 6:
                continue
            if data[0] == "id":
                continue
            if date == datetime.strptime(data[3], "%Y-%m-%d").date():
                revenue += float(data[5])

    print(f"Revenue for {date}: €{revenue:.2f}")


# Profit
def report_profit(date):
    profit = 0

    with open("sold.csv", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.split(",")
            if len(data) < 6:
                continue
            if data[0] == "id":
                continue
            if date == datetime.strptime(data[3], "%Y-%m-%d").date():
                profit += float(data[5]) - float(data[4])

    print(f"profit for {date}: €{profit:.2f}")


# PRODUCT IDs
used_ids = set()
new_ids = set()


def load_used_ids():
    try:
        with open("used_ids.csv", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if not line.isdigit():
                    continue
                used_ids.add(int(line))
    except FileNotFoundError:
        print("The 'used_ids.csv' file was not found.")


def append_new_ids():
    try:
        with open("used_ids.csv", "a", newline="") as file:
            writer = csv.writer(file)
            for new_id in new_ids:
                writer.writerow([new_id])
            new_ids.clear()
    except FileNotFoundError:
        print("The 'used_ids.csv' file was not found.")


def get_next_purchace_id():
    load_used_ids()
    try:
        last_used_id = max(used_ids, default=0)
        next_id = last_used_id + 1
        while next_id in used_ids:
            next_id += 1
        used_ids.add(next_id)
        new_ids.add(next_id)
        append_new_ids()
        return next_id
    except FileNotFoundError:
        print("The 'bought.csv' file was not found.")


# Function to validate the correct date format in the buy parse
def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return date
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Invalid expiration date. Use the format 'YYYY-MM-DD'."
        )


# Time functions
def get_current_day(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            if not data:
                return date.today()
            else:
                current_day_str = data.get("current_day", date.today())
                return datetime.strptime(current_day_str, "%Y-%m-%d").date()
    except (FileNotFoundError, json.JSONDecodeError):
        return date.today()


def write_current_time(filename, current_day):
    data = {"current_day": current_day.strftime("%Y-%m-%d")}
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print(f"{filename} file not found")


def set_date(filename, date):
    data = {"current_day": date.strftime("%Y-%m-%d")}
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print(f"{filename} file not found")
