from astrapy import DataAPIClient

client = DataAPIClient("AstraCS:WyxKmhfAiioLgOwfiyAgccBb:bf1a77e2744fe318558dd2de9b825df735f0c8d2ce569ca7e98e3bb73e5a3a48")
db = client.get_database_by_api_endpoint(
  "https://87b65a84-1bf3-4fc6-8ac4-31e8e113a2bb-us-east1.apps.astra.datastax.com"
)

print(f"Connected to Astra DB: {db.list_collection_names()}")