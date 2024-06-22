import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go

import yfinance as yf

def get_stock_data(symbol, start='2019-01-01'):
    stock_data = yf.download(symbol, start=start)
    return stock_data

def calculate_price_difference(stock_data):
    """ Year over Year, YoY"""
    # the last day's deal 
    latest_price = stock_data.iloc[-1]["Close"]
    # increase investment of the last year
    # return exact value and  percentile
    previous_year_price = stock_data.iloc[-252]["Close"] if len(stock_data) > 252 else stock_data.iloc[0]["Close"]
    price_difference = latest_price - previous_year_price
    percentage_difference = (price_difference / previous_year_price) * 100
    return price_difference, percentage_difference

def app():
    """Main code"""
    st.set_page_config(page_title="US Stock Market", layout="wide", page_icon="📈")
    hide_menu_style = "<style> footer {visibility: hidden;} </style>"
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    st.title("📈 US Stock Market")
    popular_symbols = ["AAPL",  "NVDA", "ARM", "MSFT", "AVGO","QCOM","AMZN", "GOOGL","TSLA", "META", "JPM","SMCI"]
    popular_symbols_c = {"AAPL":"Apple",  "ARM": "ARM, 安謀", "AVGO":"Boardcom", "NVDA":"Nvida, 輝達",  "MSFT":"Micosoft, 微軟", "QCOM":"Qualcomm","AMZN":" Amazon", "GOOGL":"GOOGLE", "META":"META, 元宇宙",  "SMCI": "SMCI, 美超微"}
    
    symbol = st.sidebar.selectbox("Select a Stock Symbol:", popular_symbols, index=1)

    if symbol:
        stock_data = get_stock_data(symbol)

    if stock_data is not None:
       price_difference, percentage_difference = calculate_price_difference(stock_data)
       latest_close_price = stock_data.iloc[-1]["Close"]
       max_52_week_high = stock_data["High"].tail(252).max()
       min_52_week_low = stock_data["Low"].tail(252).min()

       col1, col2, col3, col4 = st.columns(4)
       with col1:
            st.metric("Close Price", f"${latest_close_price:.2f}")
       with col2:
            st.metric("Price Difference (YoY)", f"${price_difference:.2f}", f"{percentage_difference:+.2f}%")
       with col3:
            st.metric("Yearly High", f"${max_52_week_high:.2f}")
       with col4:
            st.metric("Yearly Low", f"${min_52_week_low:.2f}")

       st.subheader(f"{symbol} Candlestick Chart") 
       candlestick_chart = go.Figure(data=[go.Candlestick(x=stock_data.index, open=stock_data['Open'], 
                              high=stock_data['High'], low=stock_data['Low'], close=stock_data['Close'])])
       candlestick_chart.update_layout(title=f"{symbol} Candlestick Chart", 
                                       xaxis_rangeslider_visible=False)
       st.plotly_chart(candlestick_chart,use_container_width=True)

       st.subheader("Summary")
       st.dataframe(stock_data.tail())

       st.download_button("Download Stock Data Overview", 
                          stock_data.to_csv(index=True), 
                          file_name=f"{symbol}_stock_data.csv", mime="text/csv")


if __name__ == "__main__":
    app()