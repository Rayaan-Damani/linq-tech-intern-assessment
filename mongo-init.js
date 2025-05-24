// MongoDB initialization script
// This runs when the MongoDB container starts for the first time

// Switch to the linq_analytics database
db = db.getSiblingDB('linq_analytics');

// Create collections
db.createCollection('sales_data');
db.createCollection('daily_aggregates');
db.createCollection('customer_segments');
db.createCollection('top_products');
db.createCollection('hourly_patterns');
db.createCollection('sales_forecast');

// Create indexes for optimal performance
db.sales_data.createIndex({ timestamp: 1 }, { name: 'timestamp_asc' });
db.sales_data.createIndex({ category: 1 }, { name: 'category_asc' });
db.sales_data.createIndex({ value: -1 }, { name: 'value_desc' });
db.sales_data.createIndex({ timestamp: 1, category: 1 }, { name: 'timestamp_category' });
db.sales_data.createIndex({ category: 1, value: -1 }, { name: 'category_value' });
db.sales_data.createIndex({ region: 1, timestamp: 1 }, { name: 'region_timestamp' });

// Create indexes for aggregate collections
db.daily_aggregates.createIndex({ date: -1 });
db.customer_segments.createIndex({ customer_type: 1 });
db.top_products.createIndex({ revenue: -1 });
db.hourly_patterns.createIndex({ hour: 1, period_type: 1 });
db.sales_forecast.createIndex({ forecast_date: 1, category: 1 });

print('✅ MongoDB initialization completed');
print('📊 Database: linq_analytics');
print('📁 Collections created: 6');
print('🔍 Indexes created: 11');