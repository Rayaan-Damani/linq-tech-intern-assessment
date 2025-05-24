import pymongo
import random
from datetime import datetime, timedelta
import argparse

def connect_to_db():
    """Connect to MongoDB - pretty straightforward"""
    try:
        client = pymongo.MongoClient('mongodb://linq-mongodb:27017/')
        db = client.linq_analytics
        print("Connected to MongoDB")
        return db
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def generate_sample_data(num_records, days_back):
    """Generate fake e-commerce data that looks realistic"""
    
    # Product categories and some sample products
    categories = {
        'Electronics': ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Camera', 'TV', 'Speaker'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes', 'Hat', 'Sweater'],
        'Books': ['Fiction Novel', 'Textbook', 'Cookbook', 'Biography', 'Manual', 'Magazine'],
        'Home & Garden': ['Chair', 'Table', 'Lamp', 'Plant', 'Tool Set', 'Decoration', 'Pillow'],
        'Sports': ['Basketball', 'Tennis Racket', 'Bicycle', 'Yoga Mat', 'Weights', 'Running Shoes'],
        'Toys': ['Board Game', 'Action Figure', 'Puzzle', 'Building Blocks', 'Doll', 'RC Car']
    }
    
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Australia']
    customer_types = ['Regular', 'Premium', 'VIP']
    payment_methods = ['Credit Card', 'PayPal', 'Cash', 'Bank Transfer']
    
    # Price ranges by category - trying to be somewhat realistic
    price_ranges = {
        'Electronics': (50, 2000),
        'Clothing': (15, 200),
        'Books': (10, 80),
        'Home & Garden': (20, 500),
        'Sports': (25, 800),
        'Toys': (5, 150)
    }
    
    records = []
    start_date = datetime.now() - timedelta(days=days_back)
    
    for i in range(num_records):
        # Pick random category and product
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        
        # Generate realistic timestamp (more sales during business hours)
        random_day = random.randint(0, days_back)
        base_date = start_date + timedelta(days=random_day)
        
        # Weight towards business hours (9 AM - 9 PM)
        if random.random() < 0.7:  # 70% chance of business hours
            hour = random.randint(9, 21)
        else:
            hour = random.randint(0, 23)
        
        timestamp = base_date.replace(
            hour=hour,
            minute=random.randint(0, 59),
            second=random.randint(0, 59),
            microsecond=random.randint(0, 999999)
        )
        
        # Generate price based on category
        min_price, max_price = price_ranges[category]
        base_price = round(random.uniform(min_price, max_price), 2)
        
        # Quantity (most orders are 1-3 items)
        qty = random.choices([1, 2, 3, 4, 5], weights=[50, 30, 15, 4, 1])[0]
        
        # Discount (not everyone gets one)
        discount = 0
        if random.random() < 0.3:  # 30% chance of discount
            discount = random.choice([5, 10, 15, 20, 25])
        
        # Calculate final value after discount
        discounted_price = base_price * (1 - discount/100)
        total_value = round(discounted_price * qty, 2)
        
        # Small chance of returns
        is_return = random.random() < 0.05  # 5% return rate
        
        record = {
            'timestamp': timestamp,
            'category': category,
            'product': product,
            'value': total_value,
            'quantity': qty,
            'region': random.choice(regions),
            'customer_type': random.choice(customer_types),
            'payment_method': random.choice(payment_methods),
            'discount_percentage': discount,
            'is_return': is_return
        }
        
        records.append(record)
        
        # Show progress every 500 records
        if (i + 1) % 500 == 0:
            print(f"Generated {i + 1} records...")
    
    return records

def main():
    parser = argparse.ArgumentParser(description='Generate sample e-commerce data')
    parser.add_argument('--records', type=int, default=1000, help='Number of records to generate')
    parser.add_argument('--days', type=int, default=30, help='Days of data to generate')
    
    args = parser.parse_args()
    
    print(f"Generating {args.records} records over {args.days} days...")
    
    # Connect to database
    db = connect_to_db()
    if not db:
        print("Could not connect to database, exiting")
        return
    
    # Generate the data
    print("Creating sample data...")
    data = generate_sample_data(args.records, args.days)
    
    # Insert into MongoDB
    try:
        collection = db.sales_data
        result = collection.insert_many(data)
        print(f"Successfully inserted {len(result.inserted_ids)} records")
        
        # Show some basic stats
        total_records = collection.count_documents({})
        total_revenue = list(collection.aggregate([
            {'$group': {'_id': None, 'total': {'$sum': '$value'}}}
        ]))[0]['total']
        
        print(f"Database now has {total_records} total records")
        print(f"Total revenue in dataset: ${total_revenue:,.2f}")
        
    except Exception as e:
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    main()