import pandas as pd
from scripts.extract import FoodPrice


class TestFoodPrice:

    def setup_method(self):
        self.food_price = FoodPrice()


    # check if the class has the api url
    def test_url(self):

        assert self.food_price.url == "https://microdata.worldbank.org/api/downloads/SOM_2021_RTFP_v02_M/files?type=data"

        print("URL test successful")


    # check if it picks the newest recent file
    def test_latest_file(self):

        data = {
            "files": [
                {
                    "filename": "SOM_RTFP_mkt_old.zip",
                    "dcdate": "2025-01-01"
                },
                {
                    "filename": "SOM_RTFP_mkt_new.zip",
                    "dcdate": "2026-01-01"
                }
            ]
        }

        latest_file = self.food_price.extract_data(data)

        assert latest_file["filename"] == "SOM_RTFP_mkt_new.zip"

        print("Latest file test successful")


    # check if the food columns change into rows
    def test_change_data(self):

        test_data = pd.DataFrame({
            "ISO3": ["SOM"],
            "country": ["Somalia"],
            "adm1_name": ["Test Region"],
            "adm2_name": ["Test District"],
            "mkt_name": ["Test Market"],
            "lat": [2.14],
            "lon": [45.12],
            "geo_id": ["test_1"],
            "price_date": ["2026-01-01"],
            "year": [2026],
            "month": [1],
            "currency": ["SOS"],
            "c_maize": [100],
            "c_milk": [100],
            "c_oil": [100],
            "c_rice": [100],
            "c_sorghum": [100]
        })

        food_prices = self.food_price.change_data(test_data)

        # 5
        assert len(food_prices) == 5

        # check the c_ was removed
        assert "maize" in food_prices["food"].values
        assert "milk" in food_prices["food"].values
        assert "oil" in food_prices["food"].values
        assert "rice" in food_prices["food"].values
        assert "sorghum" in food_prices["food"].values

        # verify the the prices are still there total 500
        assert food_prices["price"].sum() == 500

        print("Change data test successful")