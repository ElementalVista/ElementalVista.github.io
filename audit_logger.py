import pymongo
import datetime
import os

# --- Connection Details ---
USER = os.getenv("MONGO_USER", "aacuser")
PASSWORD = os.getenv("MONGO_PASS", "strongpassword123")
HOST = os.getenv("MONGO_HOST", "nv-desktop-services.apporto.com")
PORT = int(os.getenv("MONGO_PORT", "31580"))
DB_NAME = 'AAC'
COLLECTION_TO_WATCH = 'animals'
AUDIT_COLLECTION = 'audit_log'

def run_audit_log():
    """ Connects to MongoDB and starts listening for changes. """
    client = None  # Initialize client to None
    try:
        client = pymongo.MongoClient(f'mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}')
        db = client[DB_NAME]
        collection = db[COLLECTION_TO_WATCH]
        audit_collection = db[AUDIT_COLLECTION]
        print("Connected to MongoDB for auditing.")

        # Create a change stream
        with collection.watch() as stream:
            print(f"Watching collection '{COLLECTION_TO_WATCH}' for changes...")
            for change in stream:
                audit_document = {
                    "timestamp": datetime.datetime.utcnow(),
                    "operationType": change['operationType'],
                    "targetCollection": change['ns']['coll'],
                    "documentKey": change['documentKey'],
                    "fullDocument": change.get('fullDocument') # Present for insert/update
                }
                
                # Log the change to the audit collection
                audit_collection.insert_one(audit_document)
                print(f"Logged a '{change['operationType']}' operation to the audit log.")

    except pymongo.errors.PyMongoError as e:
        print(f"A MongoDB error occurred: {e}")
    except KeyboardInterrupt:
        print("\nAudit logger stopped.")
    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    run_audit_log()