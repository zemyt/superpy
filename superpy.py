from argparse import *
from datetime import date
from functions import *

__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

current_day_file = "date.json"

# Parser
parser = ArgumentParser(description="SuperpyMarket Management Tool")
subparsers = parser.add_subparsers(dest="command")

# Buy parser
buy_parser = subparsers.add_parser("buy", help="Buy product")
buy_parser.add_argument(
    "-n", "--product-name", required=True, type=str, help="Name of the product you buy"
)
buy_parser.add_argument(
    "-p", "--price", required=True, type=float, help="Price of the product you buy"
)
buy_parser.add_argument(
    "-a", "--amount", required=True, type=int, help="Amount of the product you buy"
)
buy_parser.add_argument(
    "-exp",
    "--expiration-date",
    type=validate_date,
    help="Expiration date of the product you buy (format: 'YYYY-MM-DD')",
)

# Sell parser
sell_parser = subparsers.add_parser("sell", help="Sell product")
sell_parser.add_argument(
    "-n", "--product-name", required=True, type=str, help="Name of the product you sell"
)
sell_parser.add_argument(
    "-p", "--price", required=True, type=float, help="Price of the product you sell"
)
sell_parser.add_argument(
    "-a", "--amount", required=True, type=int, help="Amount of the product you sell"
)

# Report parser
report_parser = subparsers.add_parser(
    "report", help="Generate report [inventory, revenue, profit]"
)
report_parser.add_argument(
    "report_type", type=str, help="Specify type of report [inventory, revenue, profit]"
)
report_parser.add_argument(
    "--now", action="store_true", help="Show inventory for today"
)
report_parser.add_argument(
    "--today", action="store_true", help="Show inventory for today"
)
report_parser.add_argument(
    "--yesterday", action="store_true", help="Show inventory for yesterday"
)
report_parser.add_argument(
    "--date", type=str, help="Show inventory for specific date (format: 'YYYY-MM-DD')"
)

# Advance time parser
advance_time_parser = subparsers.add_parser(
    "advance-time", help="Travel through time, and adjust the time"
)
advance_time_parser.add_argument(
    "-adv", "--advance", type=int, help="Advances time by amount of days [-1,0,1,2,etc]"
)

# Set current time parser
current_time_parser = subparsers.add_parser(
    "set-current-time", help="Set time to current time"
)

# Set Date parser
set_date_parser = subparsers.add_parser(
    "set-date",
    help="Set the date to requested date",
)
set_date_parser.add_argument(
    "-d",
    "--date",
    type=validate_date,
    help="Set the date (format: 'YYYY-MM-DD')",
)

# Parse
args = parser.parse_args()

if args.command == "buy":
    buy_product(args.product_name, args.price, args.amount, args.expiration_date)

if args.command == "sell":
    sell_product(args.product_name, args.price, args.amount)

if args.command == "report":
    if args.report_type.lower() == "inventory":
        current_date = get_current_day(current_day_file)
        if args.now or args.today:
            report_inventory(current_date)
        elif args.yesterday:
            yesterday = current_date - timedelta(days=1)
            report_inventory(yesterday)
        elif args.date:
            try:
                specific_date = datetime.strptime(args.date, "%Y-%m-%d").date()
                report_inventory(specific_date)
            except ValueError:
                print("Incorrect date format. Use format: 'YYYY-MM-DD'.")
        else:
            report_inventory(current_date)

    if args.report_type == "revenue":
        current_date = get_current_day(current_day_file)
        if args.now or args.today:
            report_revenue(current_date)
        elif args.yesterday:
            yesterday = current_date - timedelta(days=1)
            report_revenue(yesterday)
        elif args.date:
            try:
                spef_date = datetime.strptime(args.date, "%Y-%m-%d").date()
                report_revenue(spef_date)
            except ValueError:
                print("Incorrect date format. Use format: 'YYYY-MM-DD'. TEST")
        else:
            report_revenue(current_date)

    if args.report_type == "profit":
        current_date = get_current_day(current_day_file)
        if args.now or args.today:
            report_profit(current_date)
        elif args.yesterday:
            yesterday = current_date - timedelta(days=1)
            report_profit(yesterday)
        elif args.date:
            try:
                spef_date = datetime.strptime(args.date, "%Y-%m-%d").date()
                report_profit(spef_date)
            except ValueError:
                print("Incorrect date format. Use format: 'YYYY-MM-DD'. TEST")
        else:
            report_profit(current_date)


if args.command == "advance-time":
    if args.advance:
        current_date = get_current_day(current_day_file)
        new_date = current_date + timedelta(days=args.advance)
        write_current_time(current_day_file, new_date)
        print(f"Advance time by {args.advance} days, setting date to: {new_date}.")

if args.command == "set-current-time":
    current_date = date.today()
    write_current_time(current_day_file, current_date)
    print(f"Setting date to the current date: {current_date}.")

if args.command == "set-date":
    if args.date:
        set_date_to = datetime.strptime(args.date, "%Y-%m-%d")
        set_date(current_day_file, set_date_to)
        print(f"Setting date to: {args.date}.")
