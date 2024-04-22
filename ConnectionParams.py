import weaviate
import os
import warnings
from weaviate.client import WeaviateClient
from weaviate.connect import ConnectionParams, ProtocolParams

os.environ["WCS_URL"] = "https://cptcodes-zgbkr2nf.weaviate.network"
os.environ["WCS_API_KEY"] = "4xY6X9Pjatk6gWUxkNg88Hnul1UKcqRjezkH"

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

http_params = ProtocolParams(
    scheme="https",
    host="cptcodes-zgbkr2nf.weaviate.network",
    port=443,
    secure=True,
    cafile=None  
)

grpc_params = ProtocolParams(
    scheme="grpc",
    host="cptcodes-zgbkr2nf.weaviate.network",
    port=8080,
    secure=True,
    cafile=None  
)

connection_params = ConnectionParams(
    http=http_params,
    grpc=grpc_params
)

client = WeaviateClient(connection_params)

