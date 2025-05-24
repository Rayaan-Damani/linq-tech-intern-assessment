import pymongo
from datetime import datetime

def connect_to_db():
    """Connect to MongoDB"""
    try:
        client = pymongo.MongoClient('mongodb://linq-mongodb:27017/')
        db = client.linq_analytics
        return db
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def run_daily_aggregations(db):
    """Aggregate sales data by day"""
    print("Running daily sales aggregations...")
    
    pipeline = [
        {
            '$group': {
                '_id': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$timestamp'
                    }
                },
                'total_revenue': {'$sum': '$value'},
                'transaction_count': {'$sum': 1},
                'avg_order_value': {'$avg': '$value'}
            }
        },
        {
            '$sort': {'_id': 1}
        }
    ]
    
    try:
        results = list(db.sales_data.aggregate(pipeline))
        print(f"  Processed {len(results)} days of data")
        
        # Store results in aggregated collection
        if results:
            # Clear old data first
            db.daily_aggregated.delete_many({})
            # Insert new aggregations
            db.daily_aggregated.insert_many(results)
            print("  Saved daily aggregations")
            
    except Exception as e:
        print(f"  Error in daily aggregation: {e}")

def run_category_aggregations(db):
    """Aggregate sales by product category"""
    print("Running category aggregations...")
    
    pipeline = [
        {
            '$group': {
                '_id': '$category',
                'total_revenue': {'$sum': '$value'},
                'transaction_count': {'$sum': 1},
                'avg_order_value': {'$avg': '$value'},
                'total_quantity': {'$sum': '$quantity'}
            }
        },
        {
            '$sort': {'total_revenue': -1}
        }
    ]
    
    try:
        results = list(db.sales_data.aggregate(pipeline))
        print(f"  Found {len(results)} categories")
        
        if results:
            db.category_aggregated.delete_many({})
            db.category_aggregated.insert_many(results)
            print("  Saved category aggregations")
            
    except Exception as e:
        print(f"  Error in category aggregation: {e}")

def run_regional_aggregations(db):
    """Aggregate sales by region"""
    print("Running regional aggregations...")
    
    pipeline = [
        {
            '$group': {
                '_id': '$region',
                'total_revenue': {'$sum': '$value'},
                'transaction_count': {'$sum': 1},
                'avg_order_value': {'$avg': '$value'}
            }
        },
        {
            '$sort': {'total_revenue': -1}
        }
    ]
    
    try:
        results = list(db.sales_data.aggregate(pipeline))
        print(f"  Processed {len(results)} regions")
        
        if results:
            db.regional_aggregated.delete_many({})
            db.regional_aggregated.insert_many(results)
            print("  Saved regional aggregations")
            
    except Exception as e:
        print(f"  Error in regional aggregation: {e}")

def run_product_rankings(db):
    """Find top performing products"""
    print("Calculating product rankings...")
    
    pipeline = [
        {
            '$group': {
                '_id': {
                    'category': '$category',
                    'product': '$product'
                },
                'total_revenue': {'$sum': '$value'},
                'units_sold': {'$sum': '$quantity'},
                'transaction_count': {'$sum': 1}
            }
        },
        {
            '$sort': {'total_revenue': -1}
        },
        {
            '$limit': 50  # Top 50 products
        }
    ]
    
    try:
        results = list(db.sales_data.aggregate(pipeline))
        print(f"  Ranked top {len(results)} products")
        
        if results:
            db.product_rankings.delete_many({})
            db.product_rankings.insert_many(results)
            print("  Saved product rankings")
            
    except Exception as e:
        print(f"  Error in product ranking: {e}")

def main():
    print("Starting data transformations...")
    
    db = connect_to_db()
    if not db:
        print("Could not connect to database")
        return
    
    # Check if we have data to work with
    total_records = db.sales_data.count_documents({})
    print(f"Found {total_records} sales records to process")
    
    if total_records == 0:
        print("No data found - run data ingestion first")
        return
    
    # Run all the aggregations
    run_daily_aggregations(db)
    run_category_aggregations(db)
    run_regional_aggregations(db)
    run_product_rankings(db)
    
    print("All transformations completed successfully")

if __name__ == "__main__":
    main()