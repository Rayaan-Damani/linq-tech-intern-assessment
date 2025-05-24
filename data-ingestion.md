# Data Ingestion

## Overview

The `data_ingest.py` script generates realistic e-commerce transaction data and stores it in MongoDB.

## Data Structure

Each transaction includes:
- `timestamp` - when the sale occurred
- `category` / `product` - what was sold
- `value` - sale amount after discounts
- `quantity` - items sold
- `region` - geographic location
- `customer_type`, `payment_method` - customer details
- `discount_percentage`, `is_return` - transaction details

## Usage

```bash
# Generate 2000 records over 30 days
docker exec linq-python python data_ingest.py --records 2000 --days 30
```

## Approach

I focused on making the data realistic:
- Business hours bias (70% of sales 9 AM - 9 PM)
- Category-based pricing ranges
- Weighted quantity distribution (most orders 1-3 items)
- 30% discount rate, 5% return rate

The script spreads transactions randomly across the specified date range and shows progress as it runs.