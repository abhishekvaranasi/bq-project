from directory_search import get_files
from pprint import pprint
from business import is_exist
from yaml_parser import Parse_Yaml
from main import client, PROJECTID
from google.cloud import bigquery


class BQDataset():

    def __init__(self, yml, dir=""):

        self.yml = yml
        self.dir = dir

        # Gathering data
        self.parse_file = Parse_Yaml(self.yml, dir=self.dir)
        self.dataset_id = self.parse_file.dataset_id()
        self.labels = self.parse_file.labels()
        self.dataset_ref = client.dataset(self.dataset_id)

    # Creating views
    def create_dataset(self):
        # Dataset reference
        dataset = bigquery.Dataset(self.dataset_ref)

        if self.labels:
            # assigning dataset labels
            dataset.labels = self.labels
        if is_exist(self.dataset_id) == False:
            dataset = client.create_dataset(dataset)
            print("dataset {} created".format(self.dataset_id))
        else:
            print("dataset {} already exist.".format(self.dataset_id))

    def delete_dataset(self):
        try:
            client.delete_dataset(self.dataset_ref)
            print("view {} deleted.".format(self.dataset_id))
        except Exception as e:
            print(e.errors[0]['message'])
        