# Imports
from argparse import *
import csv
from datetime import date
from functions import buy_product, sell_product

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# # Your code below this line.
# def main():
#     pass

# Parser
parser = ArgumentParser(description="SuperpyMarket Management Tool")
subparsers = parser.add_subparsers(dest="command")

# Buy parser
buy_parser = subparsers.add_parser("buy", help="Buy product")

buy_parser.add_argument("--product-name", type=str, help="Name of the product you buy")
buy_parser.add_argument("--price", type=float, help="Price of the product you buy")
buy_parser.add_argument("--expiration-date", help="Expiration date of the product you buy")

# Sell parser
sell_parser = subparsers.add_parser("sell", help="Sell product")

sell_parser.add_argument("--product-name", type=str, help="Name of the product you sell")
sell_parser.add_argument("--price", type=float, help="Price of the product you sell")

# Report parser
report_parser = subparsers.add_parser("report", help="Generate report [inventory, revenue, profit]")

report_parser.add_argument("report_type", type=str, help="Specify type of report [inventory, revenue, profit]")
report_parser.add_argument("report_time", type=str, help="Specify the time you want the report of [--now --today --tomorrow --yesterday --date] ")

# Advance time parser
advance_time_parser = subparsers.add_parser("advance-time", help="Advances time")

advance_time_parser.add_argument("advance_by_day", type=int, help="Advance time, 1==1day")

# Parse
args = parser.parse_args()

if args.command == "buy":
    # buy_product(args.product_name, args.price, args.expiration_date)
    print(args.product_name)
    print(args.price)
    print(args.expiration_date)

if args.command == "sell":
    # sell_product(args.product_name, args.price)
    print(args.product_name)
    print(args.price)
    

if args.command == "report":
    if args.report_type.lower() == "inventory" or args.report_type == "revenue" or args.report_type == "profit":
        if args.report_type == "inventory":
            print("ok")
            # report_inventory()
        if args.report_type == "revenue":
            print("ok")
            # report_revenue()
        if args.report_type == "profit":
            print("ok")
            # report_profit()

    else:
        print(args.report_type.lower())
        print(f"Incorrect report type. Please select: inventory, revenue or profit.")
        

if args.command == "advance-time":
    print(args.advance_by_day)



# if __name__ == "__main__":
#     main()
