from os import environ

from dotenv import load_dotenv
from algoliasearch.search_client import SearchClient

load_dotenv()
ALGOLIA_APP_ID = 'UU6624ZJAJ'
ALGOLIA_API_KEY = environ.get('ALGOLIA_API_KEY')

client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

def search_property(location, kind, price_min, price_max, sale, address, bathrooms, rooms, furnished):
    properties = client.init_index('properties')
    filter_params = dict()
    params = ''
    def add_filter(new_filter):
        filters = filter_params.get('filters')
        if filters == None:
            filter_params['filters'] = new_filter
        else:
            filter_params['filters'] += f' AND {new_filter}'

    if price_min != None and price_max != None:
        add_filter(f"price:{price_min} TO {price_max}")
    elif price_max != None:
        add_filter(f"price < {price_max}")
    elif price_min != None:
        add_filter(f"price > {price_min}")
    
    if sale != None:
        is_sale = 1 if sale == 'true' else 0
        add_filter(f"sale={is_sale}")

    if furnished != None:
        has_furnish = 1 if furnished == 'true' else 0
        add_filter(f"furnished={has_furnish}")

    if location != None and location != 'null':
        add_filter(f"location: {location}")

    if address != None and address != 'null':
        params += address

    if kind != None and kind != 'null':
        params += f' {kind}'

    return properties.search(params, filter_params)

def create_or_update_property(**params):
    if type(params['sale']) == str:
        params['sale'] = True if params['sale'] == 'true' else False

    if type(params['heating']) == str:
        params['heating'] = True if params['heating'] == 'true' else False

    if type(params['equipped_kitchen']) == str:
        params['equipped_kitchen'] = True if params['equipped_kitchen'] == 'true' else False
    
    if type(params['furnished']) == str:
        params['furnished'] = True if params['furnished'] == 'true' else False

    if type(params['pets']) == str:
        params['pets'] = True if params['pets'] == 'true' else False

    properties = client.init_index('properties')
    properties.save_object(params)

def delete_property(property_id):
    properties = client.init_index('properties')
    properties.delete_object(property_id)
