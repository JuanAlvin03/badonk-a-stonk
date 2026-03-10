import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(layout="wide")

ticker = 'AAPL'
stockdf = yf.download(ticker, start='2023-01-01', end='2024-01-01')

fig = go.Figure(data=[go.Candlestick(x=stockdf.index,
                open=stockdf['Open'][ticker],
                high=stockdf['High'][ticker],
                low=stockdf['Low'][ticker],
                close=stockdf['Close'][ticker])])

#fig.update_layout(xaxis_rangeslider_visible=False)
#st.markdown('### <Ticker>: <Stock/company Name>')

col1, col2 = st.columns([3, 1])

col1.markdown(f'### ${ticker}: <Stock/company Name>')
col1.markdown('### Latest price: $XXX.XX (XX.XX%)')
col1.plotly_chart(fig, width='stretch')
col1.write("Candlestick chart for stock data, put average, volume, etc.")
col1.write("Time control for chart")

col2.markdown('#### Current Date/Time')
col2.subheader("A narrow column with the data")
col2.write("Financial info for ticker/stock")
