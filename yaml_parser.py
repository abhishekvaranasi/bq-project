import yaml
import os
from pprint import pprint


class Parse_Yaml():
    resources = dict()

    def __init__(self, file, dir=""):
        self.dir = dir
        self.file = file
        with open(os.path.join(os.getcwd(), self.dir, self.file), 'r') as f:
            obj = yaml.safe_load(f)
            self.resources = obj["resources"][0]

    def project_id(self):
        try:
            return self.resources['properties']["tableReference"]["projectId"]
        except:
            return self.resources['properties']["datasetReference"]["projectId"]

    def table_name(self):
        return self.resources['name'].replace("-", "_")

    def dataset_id(self):
        try:
            return self.resources['properties']["datasetId"]
        except:
            return self.resources['properties']["datasetReference"]["datasetId"]

    def labels(self):
        try:
            return self.resources['properties']["labels"]
        except:
            return False

    def schema(self):
        try:
            return self.resources['properties']['schema']["fields"]
        except:
            return False
    def query(self):
        try:
            return self.resources['properties']["view"]["query"]
        except:
            return False

    def type(self):
        try: 
            return self.resources["type"]
        except:
            return False