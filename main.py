import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(layout="wide")

#st.markdown('### <Ticker>: <Stock/company Name>')

col1, col2 = st.columns([3, 1])

col1.markdown('### <Ticker>: <Stock/company Name>')
col1.subheader("A wide column with a chart")
col1.write("Candlestick chart for stock data, put average, volume, etc.")
col1.write("Time control for chart")

col2.markdown('#### Current Date/Time')
col2.subheader("A narrow column with the data")
col2.write("Financial info for ticker/stock")

