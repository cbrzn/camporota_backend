from os import environ

from dotenv import load_dotenv
from algoliasearch.search_client import SearchClient

load_dotenv()
ALGOLIA_APP_ID = 'UU6624ZJAJ'
ALGOLIA_API_KEY = environ.get('ALGOLIA_API_KEY')

client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

def search_property(params):
    properties = client.init_index('properties')
    return properties.search(params)

def create_or_update_property(**params):
    properties = client.init_index('properties')
    properties.save_object(params)

def delete_property(property_id):
    properties = client.init_index('properties')
    properties.delete_object(property_id)
