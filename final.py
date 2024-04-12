import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from image_classifier import resize_image, classify_digit

API_KEY = "CG-UACkR7skQ5miLA3i8zrRVyBE"


def get_data(coin_name, days):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart?vs_currency=usd&days={days}"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": API_KEY
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except requests.exceptions.RequestException as e:
        st.error("Error fetching data. Please enter a valid cryptocurrency name.")
        return None


def plot_price_chart(df1, df2, coin_name1, coin_name2):
    plt.figure(figsize=(10, 6))
    plt.plot(df1['timestamp'], df1['price'], label=coin_name1, marker='o', linestyle='-')
    plt.plot(df2['timestamp'], df2['price'], label=coin_name2, marker='o', linestyle='-')
    plt.title('Price Comparison')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    st.pyplot()


def max_min_price(df):
    max_price = df['price'].max()
    min_price = df['price'].min()
    max_date = df[df['price'] == max_price]['timestamp'].iloc[0]
    min_date = df[df['price'] == min_price]['timestamp'].iloc[0]
    st.write(f"Maximum price: ${max_price:.2f} on {max_date}")
    st.write(f"Minimum price: ${min_price:.2f} on {min_date}")


def classify_image(uploaded_file):
    image = Image.open(uploaded_file)
    digit = classify_digit(image)
    st.write(f"The digit in the image is: {digit}")


def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.sidebar.title('Navigation')
    app_selection = st.sidebar.radio("Go to", ('Cryptocurrency Stock Details', 'Crypto Price Comparison', 'Image Classifier'))

    if app_selection == 'Cryptocurrency Stock Details':
        st.title('Cryptocurrency Stock Details')

        coin_name = st.text_input("Enter a cryptocurrency name:").lower()
        if st.button('Get Details'):
            if coin_name:
                st.write(f"Fetching details for {coin_name}...")
                df = get_data(coin_name, 365)
                if df is not None:
                    plt.figure(figsize=(10, 6))
                    plt.plot(df['timestamp'], df['price'], marker='o', linestyle='-')
                    plt.title('Price Over Last Year')
                    plt.xlabel('Date')
                    plt.ylabel('Price (USD)')
                    plt.grid(True)
                    st.pyplot()
                    max_min_price(df)
            else:
                st.warning("Please enter a cryptocurrency name.")
    elif app_selection == 'Crypto Price Comparison':
        st.title('Crypto Price Comparison')

        coin_name1 = st.text_input("Enter first cryptocurrency name:").lower()
        coin_name2 = st.text_input("Enter second cryptocurrency name:").lower()
        timeframe = st.radio("Choose timeframe:", ["1 week", "1 month", "1 year"])

        if st.button('Compare Prices'):
            if coin_name1 and coin_name2:
                if timeframe == "1 week":
                    days = 7
                elif timeframe == "1 month":
                    days = 30
                elif timeframe == "1 year":
                    days = 365

                coin_df1 = get_data(coin_name1, days)
                coin_df2 = get_data(coin_name2, days)

                if coin_df1 is not None and coin_df2 is not None:
                    plot_price_chart(coin_df1, coin_df2, coin_name1, coin_name2)
                    max_min_price(coin_df1)
                    max_min_price(coin_df2)
    elif app_selection == 'Image Classifier':
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            classify_image(uploaded_file)


if __name__ == "__main__":
    main()