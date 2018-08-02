from main import client
from google.cloud.exceptions import NotFound

# Checks existance of dataset, table, and view
def is_exist(dataset_id, table_id=None, view_id=None):
    dataset_ref = client.dataset(dataset_id)
    try:
        # Checking whether dataset exists
        dataset = client.get_dataset(dataset_ref)
        if dataset and table_id != None:
            table_ref = dataset_ref.table(table_id)
            try:
                table = client.get_table(table_ref)
                if table: return True
            except NotFound as error:
                return False
        elif dataset and view_id != None:
            view_ref = dataset_ref.table(view_id)
            try:
                view = client.get_table(view_ref)
                if view: return True
            except NotFound as error:
                return False
        return True
    except NotFound as error:
        return False        

# Checks for schema match between tables
def schema_match(original_schema, new_schema):
    o_schema = dict()
    n_schema = dict()

    for i in original_schema:
        o_schema[i.name] = o_schema.get(i.name, i.field_type.upper())
    for j in new_schema:
        n_schema[j.name] = n_schema.get(j.name, j.field_type.upper())

    if o_schema == n_schema:
        return True
    else: return False