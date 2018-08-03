import argparse
from bq_table import BQTable
from bq_directory import BQPack
from bq_view import BQView
from bq_dataset import BQDataset

def main():
    
    if args.refer and args.bulk == True:
        bulk = BQPack(args.refer+"s")
        if args.operation == "create":
            bulk.create_pack()
        elif args.operation == "delete":
            bulk.delete_pack()
        else:
            print("bulk operations has limited functionality. try -h or -help to get more information on usage")

    elif str(args.yaml).endswith(tuple(["yml","yaml"])) and args.bulk != True:
        if args.refer == "dataset":
            dataset = BQDataset(args.yaml)
            if args.operation == "create":
                dataset.create_dataset()
            elif args.operation == "delete":
                dataset.delete_dataset()
            else:
                print("Limited functionality. -h or -help to get more information on usage")
    
        elif args.refer == "table":
            table = BQTable(args.yaml)
            if args.operation == "create":
                table.create_table()
            elif args.operation =="delete":
                table.delete_table()
            elif args.operation == "refresh":
                table.refresh_table()
            elif args.operation == "load_data" :
                if str(args.json).endswith(".json"):
                    table.load_data(args.json)
                else:
                    print ("json file is required")
            elif args.operation == "load_table":
                table.load_table(args.table)
            elif args.operation == "backup_table":
                table.backup_table()
            elif args.operation == "load_backup":
                table.load_backup()
            else:
                print("-h or -help to get more information on usage") 

        elif args.refer == "view":
            view = BQView(args.yaml)
            if args.operation == "create":
                view.create_view()
            elif args.operation == "delete":
                view.delete_view()
            else:
                print("Limited functionality. -h or -help to get more information on usage")
    else:
        print("-h or -help to get more information on usage")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="big query operations")
    parser.add_argument("refer", help="operation towards", type=str, choices=["table","view","dataset"])    
    parser.add_argument("--bulk", help="creating all from directory", action="store_true" )
    parser.add_argument("--yaml", help="yaml file to create or update table", type=str)
    parser.add_argument("operation", nargs="?", help="yaml argument mandatory when one of these specified", type=str,  choices=["create", "delete", "refresh","load_table", "load_data", "backup_table","load_backup"])
    parser.add_argument("--json", help="json file to load data", type=str)
    parser.add_argument("--table", help="source table from which data to be copied", type=str)

    args = parser.parse_args()
    # if args.table == None and args.create.endswith(tuple(["yml","yaml"])):
    #     print(args.create)
    main()