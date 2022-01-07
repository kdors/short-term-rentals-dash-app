import os
import pandas as pd
from sodapy import Socrata
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
APP_TOKEN = os.getenv('APP_TOKEN')

def get_df():
    client = Socrata("data.nola.gov",
                    app_token=APP_TOKEN,
                    username=USERNAME,
                    password=PASSWORD)


    results = client.get("en36-xvxg", where="current_status!='Duplicate'", limit=30000)

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)
    # clean
    df = df.drop(df.loc[df["current_status"] == "Duplicate"].index)
    df = df.drop(df.loc[df["application_date"].isnull()].index)
    df["application_date"] = pd.to_datetime(df["application_date"])
    df["Year"] = pd.DatetimeIndex(df["application_date"]).year

    return df
