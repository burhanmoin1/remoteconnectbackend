from mongoengine import connect
from models import Freelancer

from pymongo import MongoClient

# Connect using mongoengine
connect('Remoteconnect')

# Connect using pymongo to access raw MongoDB commands
client = MongoClient('mongodb://localhost:27017/')  # Adjust the URI as needed
db = client['Remoteconnect']  # Use your database name
collection = db['freelancer']  # Use your collection name

# Get and print indexes
indexes = collection.list_indexes()
for index in indexes:
    print(index)

# If you need to use explain, you can still use mongoengine
from pprint import pprint

# Assuming you already have your query object
explain_output = Freelancer.objects(email='example@example.com').explain()

# Pretty print the explain output
pprint(explain_output)