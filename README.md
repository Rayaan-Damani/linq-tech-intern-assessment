# Linq Technology Intern Assessment

This is my submission for the Linq Technology Intern position. I built an e-commerce analytics system using MongoDB, Python, and Grafana with Docker.

## What I Built

I created a system that generates fake e-commerce data and shows analytics dashboards. The main components are:

- **MongoDB database** - stores sales transactions
- **Python scripts** - generate sample data and run analytics  
- **Grafana dashboard** - visualizes the data (or tries to...)
- **Docker** - runs everything in containers

## Quick Start

If you want to run this locally:

```bash
# Start everything
docker-compose up -d

# Set up the database
docker exec linq-python python datastore_setup.py

# Generate some sample data
docker exec linq-python python data_ingest.py --records 2000 --days 30

# Run data transformations
docker exec linq-python python transformations.py
```

Then go to http://localhost:3000 for Grafana (admin/admin).

## Files Overview

- `datastore_setup.py` - Sets up MongoDB collections and indexes
- `data_ingest.py` - Generates realistic e-commerce transaction data
- `transformations.py` - Aggregates data for analytics
- `docker-compose.yml` - Defines all the services
- `grafana/` - Dashboard configuration files

## Technical Notes

I ran into some issues with the Grafana MongoDB plugin compatibility. The data pipeline works fine and I can query everything through Python, but getting it to show up in Grafana was trickier than expected. The dashboard layout is there, but you might see "No data" messages.

The actual data is definitely there though - you can verify by running:
```bash
docker exec linq-python python -c "import pymongo; client = pymongo.MongoClient('mongodb://linq-mongodb:27017/'); print('Records:', client.linq_analytics.sales_data.count_documents({}))"
```

## What I Learned

This was my first time working with:
- MongoDB aggregation pipelines
- Docker multi-container applications  
- Grafana dashboard configuration
- Generating realistic sample data

The hardest part was definitely getting all the pieces to talk to each other properly, especially the Grafana datasource configuration. I did use some videos to guide me. I hope this is okay, as I am assuming that using these resources in office would be normal and encouraged. I hope this also displayed my ability to being a quick learner. 

## Requirements Met

- Database setup with proper indexing
- Data ingestion pipeline  
- Analytics and transformations
- Visualization dashboard (layout complete)
- Docker containerization
- Documentation

Thanks for taking the time to review this!