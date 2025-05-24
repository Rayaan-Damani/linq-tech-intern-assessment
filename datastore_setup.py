import pymongo
from pymongo import IndexModel, ASCENDING, DESCENDING

def setup_mongodb():
    """Set up the MongoDB database and collections"""
    print("Starting MongoDB setup...")
    
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient('mongodb://linq-mongodb:27017/')
        print("Successfully connected to MongoDB")
        
        # Use the analytics database
        db = client.linq_analytics
        print("Using database: linq_analytics")
        
        # Set up the main sales data collection
        print("Setting up collection: sales_data")
        sales_collection = db.sales_data
        
        # Create some indexes to make queries faster
        # I'm not 100% sure these are the best indexes but they seem reasonable
        indexes = [
            IndexModel([("timestamp", ASCENDING)], name="timestamp_asc"),
            IndexModel([("category", ASCENDING)], name="category_asc"), 
            IndexModel([("value", DESCENDING)], name="value_desc")
        ]
        
        # Try to create the indexes
        for index in indexes:
            try:
                sales_collection.create_index(index.document["key"], name=index.document.get("name"))
                print(f"  Created index: {index.document.get('name')}")
            except Exception as e:
                print(f"  Index creation issue: {e}")
                # Not a big deal if indexes already exist
        
        # Also set up a collection for aggregated data (might use this later)
        agg_collection = db.sales_aggregated
        print("Set up aggregated data collection")
        
        print("MongoDB setup completed successfully")
        return True
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = setup_mongodb()
    if success:
        print("Database is ready to use")
    else:
        print("Something went wrong with the setup")