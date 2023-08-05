# flake8: noqa
import time
import os
from azurebatchload import UploadBatch
from azurebatchload.download import DownloadBatch

# from azurebatchload.utils import Utils
from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)

# if not os.environ.get("AZURE_STORAGE_CONNECTION_STRING"):
#     raise ValueError("No connection string")


source = "/Users/erfannariman/Workspace/zypp/azure-batch-load/data"
account_key = os.environ.get("account_key")
account_name = os.environ.get("account_name")
# az_batch = UploadBatch(destination="test", source=source, pattern="*.PDF")
# az_batch.upload()


start = time.time()
az_batch = DownloadBatch(
    destination="data/",
    source="twinfield",
    folder="xml_responses/vrk/20210330/",
    method="single",
)
az_batch.download()
print(time.time() - start)

# az_batch = Utils(container="mailadapter")
# files = az_batch.list_files()
# print(files)
