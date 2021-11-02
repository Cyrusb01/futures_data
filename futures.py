from binance.client import Client
import requests 
import json
import pandas as pd 
import time 
import streamlit as st
import yfinance as yf
import plotly.express as px
import os
st.title("Binance Futures Visualization")

asset = st.selectbox("Which crypto would you like to see the futures for", ["BTC", "ETH", "ADA", "BCH", "BNB", "DOT", "LINK", "LTC", "XRP"])



def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

api_key = os.getenv("BINANCE_API")
api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(api_key, api_secret)

# btc_price = client.get_symbol_ticker(symbol="BTCBUSD")

contract_types = ["CURRENT_QUARTER", "NEXT_QUARTER", "PERPETUAL"]
type_dict = {} #will contain the type and then the item will be a pandas dataframe containing all the data
for type in contract_types:
    parameters = {
        "pair": asset.upper() + "USD",
        "contractType": type,
        "period" : "1d"

    }

    response = requests.get("https://dapi.binance.com/futures/data/basis", params=parameters)
    # jprint(response.json())

    count = 0
    data = {"timestamp": [], "future_price": [], "index_price": []}

    for data_dict in response.json():
        # print("Futures Price:", data_dict["futuresPrice"])
        data["future_price"].append(float(data_dict["futuresPrice"]))
        # print("Index Price:", data_dict["indexPrice"])
        data["index_price"].append(float(data_dict["indexPrice"]))
        data["timestamp"].append(data_dict["timestamp"])
        # count += 1
    # print(count)
    df = pd.DataFrame.from_dict(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')

    df = df.set_index("timestamp")
    # df = df[["index_price"]]
    # df.to_csv("data.csv")
    type_dict[type] = df
    # time.sleep(30)



# fig = px.line(type_dict["CURRENT_QUARTER"])
# fig.update_yaxes(range=[50000, 65000])
#########################################CURRENT QUARTER ###############################################
st.subheader("Futures Purchased to expire in the 'Current Quarter'")
st.write("The chart below shows the index price and futures price for the last 200 days")
st.line_chart(type_dict["CURRENT_QUARTER"])
df= type_dict["CURRENT_QUARTER"]
df["premium"] =  ((df["future_price"]/df["index_price"]) - 1) * 100
st.write("The bar chart shows the premiums of the future price, ie: future price/ index price ")
st.bar_chart(df["premium"])

#########################################NEXT QUARTER ###############################################
st.subheader("Futures Purchased to expire in the 'Next Quarter'")
st.write("The chart below shows the index price and futures price for the last 200 days")
st.line_chart(type_dict["NEXT_QUARTER"])
df= type_dict["NEXT_QUARTER"]
df["premium"] =  ((df["future_price"]/df["index_price"]) - 1) * 100
st.write("The bar chart shows the premiums of the future price, ie: future price/ index price ")
st.bar_chart(df["premium"])

#########################################CURRENT QUARTER ###############################################
st.subheader("Perpetual Futures")
st.write("The chart below shows the index price and futures price for the last 200 days")
st.line_chart(type_dict["PERPETUAL"])
df= type_dict["PERPETUAL"]
df["premium"] =  ((df["future_price"]/df["index_price"]) - 1) * 100
st.write("The bar chart shows the premiums of the future price, ie: future price/ index price ")
st.bar_chart(df["premium"])
st.dataframe(df)

# st.dataframe(df)
# msft = yf.download("MSFT")

# df = pd.DataFrame(msft)
# df = df[["Close"]]
# print(df)
# st.line_chart(df)
# st.dataframe(df)