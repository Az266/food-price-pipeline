import mysql.connector

import pandas as pd

from db_connection import connection

#### Connect to mysql
def connect():
    try:
        db = connection()
        cursor = db.cursor()
        print("Connected to MySQL")
        return db , cursor
    except mysql.connector.Error as error:
        print(f"Database connection failed: {error}")
        return None, None

## read csv

def read_file():
    df = pd.read_csv("data/datacsv/food_prices.csv")
    return df


def save_market(df, cursor):

    market_df = df[
        ["geo_id", "mkt_name", "adm1_name", "adm2_name", "lat", "lon"]
    ].drop_duplicates()

    print(market_df.shape)

    insert_market = """
    INSERT IGNORE INTO dim_market
    (geo_id, mkt_name, adm1_name, adm2_name, lat, lon)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for index, row in market_df.iterrows():

        lat = row["lat"]
        lon = row["lon"]

        if pd.isna(lat):
            lat = None

        if pd.isna(lon):
            lon = None

        values = (
            row["geo_id"],
            row["mkt_name"],
            row["adm1_name"],
            row["adm2_name"],
            lat,
            lon
        )

        cursor.execute(insert_market, values)


def save_commodity(df, cursor):
     commodity_df = df[["food"]].drop_duplicates()
     print(commodity_df)
     insert_commodity = """
     INSERT IGNORE INTO  dim_commodity (commodity_name)
     VALUES (%s)
     """
     
     for _, row in commodity_df.iterrows():
        values = (
            row["food"],
            )
            
        cursor.execute(insert_commodity, values)
      

# print("Commodities inserted successfully")


############ Date 

def save_date(df, cursor):
    date_df = df[
        ["price_date", "year", "month"]
        ].drop_duplicates()
        # print(date_df.shape)
        # print(date_df.head())
        
    insert_date = """
    INSERT IGNORE INTO dim_date
    (price_date, year, month)
    VALUES (%s, %s, %s)"""
        
    for _, row in date_df.iterrows():
        values = (
            row["price_date"],
            int(row["year"]),
            int(row["month"])
            )
        cursor.execute(insert_date, values)
               


def get_ids(cursor):

    # Get market IDs
    cursor.execute("""
        SELECT market_id, geo_id
        FROM dim_market
    """)

    market_rows = cursor.fetchall()
    market_ids = {}

    for row in market_rows:
        market_id = row[0]
        geo_id = row[1]

        market_ids[geo_id] = market_id


    # Get commodity IDs
    cursor.execute("""
        SELECT commodity_id, commodity_name
        FROM dim_commodity
    """)

    commodity_rows = cursor.fetchall()
    commodity_ids = {}

    for row in commodity_rows:
        commodity_id = row[0]
        commodity_name = row[1]

        commodity_ids[commodity_name] = commodity_id


    # Get date IDs
    cursor.execute("""
        SELECT date_id, price_date
        FROM dim_date
    """)

    date_rows = cursor.fetchall()
    date_ids = {}

    for row in date_rows:
        date_id = row[0]
        price_date = row[1]

        price_date = str(price_date)

        date_ids[price_date] = date_id


    return market_ids, commodity_ids, date_ids


    ##########################
if __name__ == "__main__":

    db, cursor = connect()

    if db is not None:

        df = read_file()

        save_market(df, cursor)
        save_commodity(df, cursor)
        save_date(df, cursor)

        market_ids, commodity_ids, date_ids = get_ids(cursor)

        db.commit()

        cursor.close()
        db.close()

        print("Database loaded successfully")