import os
import tempfile
import shutil
import os
import zipfile
import tarfile
from contextlib import contextmanager
import requests

ARTIFACTORY_BASE_URL = "https://104.196.181.115/artifactory/libs-snapshot-local/com/globalpayments/businessview"


directories = ["datasets","tables","views"]
accepted_extensions = [".yaml", ".yml"]

@contextmanager
def mktmpdir():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)

# headers = {'X-Jfrog-Art-Api': os.environ['ARTIFACTORY_KEY']}

with mktmpdir() as tmpdir:
    # r = requests.get(
    #     ARTIFACTORY_BASE_URL, headers=headers, verify=False, stream=True)
    # local_path = os.path.join(tmpdir,"tar")

    # # Writes artifactory results to temp directory
    # with open(local_path, "wb") as f:
    #     for chunk in r.iter_content(chunk_size=512):
    #         if chunk:
    #             f.write(chunk)

    service_path = os.path.join(tmpdir, "yaml")
    # print(service_path)
    local_path  = os.path.join(os.getcwd(), "BQTableYamlFile_94.tar")
    # print(local_path)
    tar = tarfile.open(local_path)
    tar.extractall(service_path)
    # print(os.listdir(service_path))
# service_archive = zipfile.ZipFile(local_path, mode="r")
# service_archive.extractall(path=service_path)
# service_archive.close()

# takes dir_name returns only yaml files in directory
def get_files(dir_name):
    if (dir_name in directories):
        return [yml for yml in os.listdir(os.path.join(os.getcwd(), dir_name)) if yml.endswith(tuple(accepted_extensions))]


