# Food price pipeline

# Somalia Food Prices ETL: World Bank API - MySQL Star Schema

A small end-to-end ETL pipeline that retrives Somalia food prices from the World Bank  API, cleans them, and loads a MySQL star schema.

## Aim

To investigate long-term food price behaviour in Somalia, exploring regional differences, and  trends across markerts over nearly two decades.

**Tech stack:** Python (Pandas, Requests, mysql-connector-python) | MySQL 8.4 | Docker Compose

## 🚀 Core Features
> - Retrieves and downloads the newest Somalia food price file from the World Bank API
> - Cleans and reshapes the raw data ~54,740 price records
> - Stores everything in four linked MySQL tables via a star schema (markets, commodities, dates, and prices)
> - Covers 46 markets and 5 staple foods (maize, milk, oil, rice, sorghum) from 2007 and onwards
> - Runs MySQL in Docker

