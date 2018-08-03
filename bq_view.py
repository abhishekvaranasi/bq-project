from directory_search import get_files
from pprint import pprint
from business import is_exist
from yaml_parser import Parse_Yaml
from main import client, PROJECTID
from google.cloud import bigquery


class BQView():

    def __init__(self, yml, dir=""):

        self.yml = yml
        self.dir = dir

        # Gathering data
        self.parse_file = Parse_Yaml(self.yml, dir=self.dir)
        self.dataset_id = self.parse_file.dataset_id()
        self.view_id = self.parse_file.table_name()
        self.labels = self.parse_file.labels()
        self.dataset_ref = client.dataset(self.dataset_id)

        # View reference
        self.view_ref = self.dataset_ref.table(self.view_id)

    # Creating views
    def create_view(self):
        pprint("Creating view: {}".format(self.view_id))

        view = bigquery.Table(self.view_ref)
        if self.labels != False:
            view.labels = self.labels
        # Gets sql query from yaml file
        sql_query = self.parse_file.query().replace("PROJECT_ID",PROJECTID)
        view.view_query = sql_query
        if is_exist(self.dataset_id, view_id=self.view_id) == False:
            view = client.create_table(view)
            print("view {} created.".format(view.full_table_id))
        else:
            print("view {} already exist.".format(self.view_id))

    def delete_view(self):
        try:
            client.delete_table(self.view_ref)
            print("view {} deleted.".format(self.view_id))
        except Exception as e:
            print(e.errors[0]['message'])
        