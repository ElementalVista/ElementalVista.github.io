from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.son import SON

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, user='aacuser', password='strongpassword123', host='nv-desktop-services.apporto.com', port=31580, db='AAC', col='animals'):
        """
        Initialize connection.
        """
        try:
            # Initialize Connection
            self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
            self.database = self.client[db]
            self.collection = self.database[col]
            print("Connected to MongoDB successfully.")
        except Exception as e:
            print(f"Error in connecting to MongoDB: {e}")

    def create(self, data):
        """ Create a document in the collection. """
        try:
            if isinstance(data, dict):
                result = self.collection.insert_one(data)
                print("Document inserted successfully.")
                return True
            else:
                raise ValueError("Invalid data format. Expected a dictionary.")
        except Exception as e:
            print(f"Error in inserting data: {e}")
            return False

    def read(self, query=None):
        """ Reads documents from the collection. """
        try:
            if query is None:
                query = {}  
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception as e:
            print(f"Error in reading data: {e}")
            return []

    def update(self, query, new_values):
        """ Update documents in the collection. """
        try:
            if isinstance(query, dict) and isinstance(new_values, dict):
                result = self.collection.update_many(query, {'$set': new_values})
                print(f"Updated {result.modified_count} document(s) successfully.")
                return result.modified_count
            else:
                raise ValueError("Invalid input format. Expected dictionaries for both query and new values.")
        except Exception as e:
            print(f"Error in updating data: {e}")
            return 0

    def delete(self, query):
        """ Delete documents from the collection. """
        try:
            if isinstance(query, dict):
                result = self.collection.delete_many(query)
                print(f"Deleted {result.deleted_count} document(s) successfully.")
                return result.deleted_count
            else:
                raise ValueError("Invalid query format. Expected a dictionary.")
        except Exception as e:
            print(f"Error in deleting data: {e}")
            return 0
            
    def aggregate(self, pipeline):
        """ Executes an aggregation pipeline. """
        try:
            if not isinstance(pipeline, list):
                raise ValueError("Invalid pipeline format. Expected a list.")
            cursor = self.collection.aggregate(pipeline)
            return list(cursor)
        except Exception as e:
            print(f"Error in aggregation: {e}")
            return []

    def call_stored_procedure(self, procedure_name, *args):
        """ Calls a stored JavaScript function. """
        try:
            result = self.database.command(SON([('$eval', f'return {procedure_name}(...{list(args)})')]))
            return result.get('retval', [])
        except Exception as e:
            print(f"Error calling stored procedure: {e}")
            return []