import argparse
from bq_table import BQTable
from bq_view import BQView
from bq_directory import BQPack
# from bq_view import BQView


def main():

    if args.create_bulk:
        bulk = BQPack(args.create_bulk)
        bulk.create_pack()
    elif str(args.yaml).endswith(tuple(["yml", "yaml"])):
        table = BQTable(args.yaml)
        if args.operation == "create":
            table.create_table()
        elif args.operation == "refresh":
            table.refresh_table()
        elif args.operation == "create_view":
            view = BQView(args.yaml)
            view.create_view()
        elif args.operation == "load_data":
            if str(args.json).endswith(".json"):
                table.load_data(args.json)
            else:
                print("json file is required")
        elif args.operation == "load_table":
            table.load_table(args.table)
        elif args.operation == "backup_table":
            table.backup_table()
        elif args.operation == "load_backup":
            table.load_backup()
        else:
            print("-h or -help to get more information on usage")
    else:
        print("-h or -help to get more information on usage")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="big query operations")
    parser.add_argument("--create-bulk", help="operation to perform",
                        type=str, choices=["datasets", "tables", "views"])
    parser.add_argument(
        "--yaml", help="yaml file to create or update table", type=str)
    parser.add_argument("operation", nargs="?", help="yaml argument mandatory when one of these specified", type=str,  choices=[
                        "create", "refresh", "create_view", "load_table", "load_data", "backup_table", "load_backup"])
    parser.add_argument("--json", help="json file to load data", type=str)
    parser.add_argument(
        "--table", help="source table from which data to be copied", type=str)

    args = parser.parse_args()
    # if args.table == None and args.create.endswith(tuple(["yml","yaml"])):
    #     print(args.create)
    main()
