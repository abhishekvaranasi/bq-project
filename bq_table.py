from directory_search import get_files
from pprint import pprint
from business import is_exist, schema_match
from yaml_parser import Parse_Yaml
from main import client, PROJECTID, BUCKETID
from google.cloud import bigquery
from datetime import datetime
import os

today = datetime.now()
right_now = today.strftime("%m_%d_%Y_%I_%M%p")

class BQTable():

    def __init__(self, yml, dir=""):

        self.yml = yml
        self.dir = dir

        # gathering data
        self.parse_file = Parse_Yaml(self.yml,self.dir)
        self.dataset_id = self.parse_file.dataset_id()
        self.table_id = self.parse_file.table_name()
        self.type = self.parse_file.type()

        # dataset reference
        self.dataset_ref = client.dataset(self.dataset_id, project=PROJECTID)

        # table reference
        self.table_ref = self.dataset_ref.table(self.table_id)


    # Creating single table
    def create_table(self):
        if self.type.endswith(".table"):
            new_schema = [bigquery.SchemaField(
                field["name"], field["type"]) for field in self.parse_file.schema()]

            table = bigquery.Table(self.table_ref, schema=new_schema)
            # assigning dataset labels
            table_lables = self.parse_file.labels()
            if table_lables != False:
                table.labels = table_lables
            if is_exist(self.dataset_id, table_id = self.table_id) == True:
                get_table = client.get_table(self.table_ref)
                original_schema = get_table.schema
                if schema_match(original_schema, new_schema):
                    pass
                else:
                    print("Recreating table {} with new schema...".format(self.table_id))
                    try:
                        table = client.update_table(table,['schema'])
                    except:
                        print("You cannot perform remove column operation on {}. Please delete and recreate table.".format(self.table_id))
            else:
                table = client.create_table(table)
                print("table {} created.".format(table.table_id))
        else:
            print("Looks like it's not a table. Please check the yaml file.")

    def delete_table(self):
        try:
            client.delete_table(self.table_ref)
            print("table {} deleted".format(self.table_id))
        except Exception as e:
            print(e.errors[0]['message'])

    # updating table with new schema
    def update_table(self):
        if is_exist(self.dataset_id, table_id=self.table_id) == True:
            table = client.get_table(self.table_ref)
            original_schema = table.schema
            new_schema = [bigquery.SchemaField(
                field["name"], field["type"]) for field in self.parse_file.schema()]

            if schema_match(original_schema, new_schema):
                pass
            else:
                print("Recreating table {} with new schema...".format(self.table_id))    
                self.create_table()
        else:
            print("table does not exist. Creating {} table...".format(self.table_id))
            self.create_table()

    # Copying / Duplicating table
    def copy_table(self):

        # table reference
        source_table_ref = self.dataset_ref.table(self.table_id)

        print("copying {} table...".format(self.table_id))
        try:
            dest_table_ref = self.dataset_ref.table(self.table_id+"{}".format(right_now))
            job = client.copy_table(source_table_ref, dest_table_ref)
        except:
            dest_table_ref = self.dataset_ref.table(self.table_id+"{}".format(right_now))
            job = client.copy_table(source_table_ref, dest_table_ref)
        job.result()
        print("table {} copied successfully".format(self.table_id))

    # Loading data from external file
    def load_data(self, json):
        print("loading data from {}...".format(json))
        job_config = bigquery.LoadJobConfig()
        # job_config.autodetect = True
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        uri = os.path.join(os.getcwd(), json)
        with open(uri, 'rb') as source_file:
            job = client.load_table_from_file(
                source_file, 
                self.table_ref, 
                job_config=job_config)
        job.result()
        print("data loaded into {}.".format(self.table_id))


    # Loading data from other table
    def load_table(self, source_table):

        job_config = bigquery.QueryJobConfig()
        job_config.destination = self.table_ref
        # job_config.use_legacy_sql = True

        sql = """
            SELECT * 
            FROM `{}.{}.{}`
            """.format(PROJECTID, self.dataset_id, source_table)
        print("loading data from {} to {}".format(source_table, self.table_id))
        query_job = client.query(sql, job_config=job_config)
        query_job.result()
        print("data loaded successfully!")

    # backup table data into bucket
    def backup_table(self):
        
        destination_uri = 'gs://{}/{}.json'.format(BUCKETID, self.table_id + right_now)
        job_config = bigquery.job.ExtractJobConfig()
        job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON
        print("backing up data from {} to {}".format(self.table_id, destination_uri))
        backup_job = client.extract_table(self.table_ref, destination_uri, job_config=job_config)
        backup_job.result()
        print("Exported to {}:{}.{} to {}".format(PROJECTID, self.dataset_id, self.table_id, destination_uri))

    # loading backup data 
    def load_backup(self):
        job_config = bigquery.LoadJobConfig()
        # job_config.autodetect = True
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        uri = "gs://{}/{}.json".format(BUCKETID, self.table_id + right_now)
        print("loading data from {} to {}.".format(uri, self.table_id))
        load_data = client.load_table_from_uri(uri, self.table_ref, job_config=job_config)
        assert load_data.job_type == 'load'
        load_data.result()
        assert load_data.state == 'DONE'
        print("data loaded from {} to {}.".format(uri, self.table_id))

    # Updating table with new schema along with data backup
    def refresh_table(self):

        if is_exist(self.dataset_id, table_id=self.table_id) == True:
            table = client.get_table(self.table_ref)
            original_schema = table.schema
            new_schema = [bigquery.SchemaField(
                field["name"], field["type"]) for field in self.parse_file.schema()]

            if schema_match(original_schema, new_schema):
                print("Schema already exist.")
            else:
                print("Recreating table {} with new schema...".format(self.table_id))
                self.copy_table()
                self.backup_table()
                print("deleting table {}...".format(self.table_id))
                client.delete_table(self.table_ref)
                print("table {} deleted! from dataset {}.".format(
                    self.table_id, self.dataset_id))
                print("recreating table {} with new schema...".format(self.table_id))
                self.create_table()
                # self.load_table(self.table_id + right_now)
                self.load_backup()
                print("loading backed up data into the new table")

        else:
            print("table {} does not exist!".format(self.table_id))
            ask_to_create = str(input("do you want to create?: "))
            if ask_to_create.lower() == "yes":
                self.create_table()
            else:
                print("table creation cancelled!")
