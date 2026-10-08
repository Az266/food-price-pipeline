-- Create database
CREATE DATABASE IF NOT EXISTS food_prices;

-- Use database
USE food_prices;


-- ==========================================
-- Market details
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_market (
    market_id INT AUTO_INCREMENT PRIMARY KEY,
    geo_id VARCHAR(100),
    mkt_name VARCHAR(100) NOT NULL,
    adm1_name VARCHAR(100),
    adm2_name VARCHAR(100),
    lat FLOAT,
    lon FLOAT,

    UNIQUE (geo_id)
);


-- ==========================================
-- Commodity dimension
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_commodity (
    commodity_id INT AUTO_INCREMENT PRIMARY KEY,
    commodity_name VARCHAR(50) NOT NULL,

    UNIQUE (commodity_name)
);


-- ==========================================
-- Date 
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    price_date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,

    UNIQUE (price_date)
);


-- ==========================================
-- Price fact table
-- ==========================================

CREATE TABLE IF NOT EXISTS fact_price (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    market_id INT NOT NULL,
    commodity_id INT NOT NULL,
    date_id INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    currency VARCHAR(10) NOT NULL,

    FOREIGN KEY (market_id)
        REFERENCES dim_market(market_id),

    FOREIGN KEY (commodity_id)
        REFERENCES dim_commodity(commodity_id),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),

    UNIQUE (market_id, commodity_id, date_id)
);