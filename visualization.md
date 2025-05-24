# Visualization

## Approach

I set up Grafana to create analytics dashboards for the e-commerce data. The dashboard configuration is in `grafana/dashboards/linq-dashboard.json`.

## Dashboard Design

The dashboard includes:
- **Key metrics**: Total revenue, transactions, average order value, return rate
- **Trends**: Daily sales over time
- **Breakdowns**: Revenue by category and region
- **Details**: Top products table, hourly patterns

## Technical Challenge

I encountered issues with the MongoDB datasource plugin for Grafana. The plugin installation caused container crashes, and even after stabilizing, the datasource connection isn't working properly.

## Data Verification

The backend data pipeline works correctly. You can verify with:
```bash
docker exec linq-python python -c "
import pymongo
client = pymongo.MongoClient('mongodb://linq-mongodb:27017/')
print('Records:', client.linq_analytics.sales_data.count_documents({}))
"
```

## Access

- URL: http://localhost:3000
- Login: admin/admin
- Dashboard: "Linq Sales Analytics"

Note: You may see "No data" messages due to the datasource connection issue, but the dashboard layout demonstrates the intended analytics approach.