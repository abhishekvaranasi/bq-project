
from directory_search import get_files
from pprint import pprint
from business import is_exist
from yaml_parser import Parse_Yaml
from main import client, PROJECTID
from google.cloud import bigquery
from bq_table import BQTable
from bq_view import BQView
from bq_dataset import BQDataset

class BQPack():

    def __init__(self, dir):
        
        self.dir = dir

    def create_pack(self):
        yaml_files = get_files(self.dir)
        for yml in yaml_files:
            parse_file = Parse_Yaml(yml, self.dir)
            yml_type = parse_file.type()
            dataset_id  = parse_file.dataset_id()
            dataset_ref = client.dataset(dataset_id)

            if str(yml_type).endswith(".dataset"):
                dataset = BQDataset(yml, self.dir)
                dataset.create_dataset()

            elif str(yml_type).endswith(".table"):
                if parse_file.schema():
                    table = BQTable(yml, self.dir)
                    table.create_table()
                else:
                    view = BQView(yml)
                    view.create_view()

        print("Execution completed!")

    def delete_pack(self):
        yaml_files = get_files(self.dir)
        for yml in yaml_files:
            parse_file = Parse_Yaml(yml, dir=self.dir)
            yml_type = parse_file.type()
            dataset_id  = parse_file.dataset_id()
            dataset_ref = client.dataset(dataset_id)

            if str(yml_type).endswith(".dataset"):
                dataset = BQDataset(yml, self.dir)
                dataset.delete_dataset()

            elif str(yml_type).endswith(".table"):
                if parse_file.schema():
                    table = BQTable(yml, self.dir)
                    table.delete_table()
                else:
                    view = BQView(yml, self.dir)
                    view.delete_view()

        print("Execution completed!")
        
    