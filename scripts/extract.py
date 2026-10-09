# extracting api  

import requests 
import zipfile
import pandas as pd


## Fetch api
class FoodPrice:

    def __init__(self):
        self.url = "https://microdata.worldbank.org/api/downloads/SOM_2021_RTFP_v02_M/files?type=data"
        
    def api(self):  
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            return data 
        except requests.RequestException as error:
                
            print(f"ApI request failed: {error}")
            
        return None
            
    def extract_data(self, data):
        price_files = []

        for file in data["files"]:
            if file["filename"].startswith("SOM_RTFP_mkt"):
                price_files.append(file)

        print(len(price_files))

        latest_file = max(
            price_files,
            key=lambda 
            file: file["dcdate"])
            
        return latest_file
        
    def download_file(self, latest_file):
        ## access the file and download
        download_url = latest_file["links"]["download"]
        print(download_url)
        try:
            file_response = requests.get(download_url)
            file_response.raise_for_status()
        except requests.RequestException as error:
            print(f"ApI request failed: {error}")
            return None
            ## save it to a at location
        zip_path = "data/raw/" + latest_file["filename"]
        with open(zip_path, "wb") as file:
            file.write(file_response.content)
            
        return zip_path
        
    ## read the zip file 
    def extract_zip(self, zip_path):
        with zipfile.ZipFile(zip_path, "r") as zip_file:
            print(zip_file.namelist())
            
            csv_name = zip_file.namelist()[0]
            
            with zip_file.open(csv_name) as csv_file:
                df = pd.read_csv(csv_file)
        return df


    # print(type(data))
    # print(data.keys())
    # print(type(data["files"]))
    # print(len(data["files"]))



    def data_read(self, df):
        print(df.shape)

        # Missing values
        missing_values = df.isnull().sum()
        print(missing_values[missing_values > 0])

        print(
            df[df["lat"].isnull()]
            ["mkt_name"]
            .value_counts()
        )

        print(
            df[df["inflation_food_price_index"].isnull()]
            .groupby("year")
            .size()
        )

        print(
            df[df["rice"].isnull()]
            .groupby("mkt_name")
            .size()
            .sort_values(ascending=False)
        )
##################### SELECTING DATA:



# for file in price_files[:5]:
#     print(file["filename"], file["dcdate"])


# print(latest_file["filename"])
# print(latest_file["dcdate"])


# download_url = latest_file["links"]["download"]

# print(download_url)

# file_response = requests.get(download_url)

# print(file_response.status_code)

# with open("data/raw/" + latest_file["filename"], "wb") as file:

# print(df.head())








############ data selction


    def select_final_data(self, df):
        print( df[ [
                "ISO3",
                "country",
                "adm1_name",
                "adm2_name",
                "mkt_name",
                "lat",
                "lon",
                "geo_id"
            ]].head(10) )

        print(df[[
                "price_date",
                "year",
                "month"
            ]].head(15) )

        # Check date columns
        print(df[["price_date", "year", "month"]].dtypes)

        # Change price_date to datetime
        df["price_date"] = pd.to_datetime(df["price_date"])

        print(df[["price_date", "year", "month"]].dtypes)
        print("Missing dates:", df["price_date"].isnull().sum())

        # Check year and month match price_date
        print("Wrong year:", (df["price_date"].dt.year != df["year"]).sum())
        print("Wrong month:", (df["price_date"].dt.month != df["month"]).sum())

        # Check currency
        print(df["currency"].value_counts(dropna=False))

        clean_df = df[
        [
            "ISO3",
            "country",
            "adm1_name",
            "adm2_name",
            "mkt_name",
            "lat",
            "lon",
            "geo_id",
            "price_date",
            "year",
            "month",
            "currency",
            "c_maize",
            "c_milk",
            "c_oil",
            "c_rice",
            "c_sorghum"
        ]
        ].copy()

        print("columns successeful", clean_df.shape)
        print(clean_df.head())
        return clean_df


    #### change item list into rows
    def change_data(self, clean_df):
        columns_keep = [ 
            "ISO3", "country",
             "adm1_name",
             "adm2_name", 
             "mkt_name",
             "lat",
             "lon",
             "geo_id",
             "price_date",
             "year",
             "month",
             "currency"
             ]

        food_columns = [
            "c_maize",
            "c_milk",
            "c_oil",
            "c_rice",
            "c_sorghum" ]

         ##Change the food columns into rows with food and price columns

        food_prices = clean_df.melt(
            id_vars=columns_keep,
            value_vars=food_columns,
            var_name="food",


            value_name="price"
        )

        # Remove c_ from the beginning of each food name
        food_prices["food"] = food_prices["food"].str[2:]


        print(food_prices.shape)
        print(food_prices.head(10))

        return food_prices


##########################################################################



    # Check the cleaned data
    def check_data(self, food_prices):

        duplicates = food_prices.duplicated(
            subset=["mkt_name", "price_date", "food"]
        ).sum()

        print("Duplicates:", duplicates)

        print("Missing prices:", food_prices["price"].isnull().sum())
        print("Zero prices:", (food_prices["price"] == 0).sum())
        print("Negative prices:", (food_prices["price"] < 0).sum())








    # Save cleaned data to CSV
    def save_data(self, food_prices):


        output_path = "data/datacsv/food_prices.csv"

        food_prices.to_csv(output_path, index=False)

        print(f"Processed data saved to: {output_path}")

    ################


if __name__ == "__main__":

    # Create the FoodPrice finall
    food_price = FoodPrice()

    # Get the API data
    data = food_price.api()

    if data is not None:

        # Find the most recent  file
        latest_file = food_price.extract_data(data)

        # Download the file
        zip_path = food_price.download_file(latest_file)

        if zip_path is not None:

            # Read the CSV  thats inside the ZIP file
            df = food_price.extract_zip(zip_path)

            # Look at the  data
            food_price.data_read(df)

            # Select and clean the columns
            clean_df = food_price.select_final_data(df)

            # Change food columns into rows
            food_prices = food_price.change_data(clean_df)

            # Check the cleanned data
            food_price.check_data(food_prices)

            # Save the cleaned data
            food_price.save_data(food_prices)