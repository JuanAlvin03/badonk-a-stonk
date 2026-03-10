import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

ticker = 'AAPL'
#stockdf = yf.download(ticker, start='2023-01-01', end='2024-01-01')
stock = yf.Ticker(ticker)
#stockdf = stock.history(period='1y')
stockdf = stock.history(period='2d', interval='15m')

# Intervals: Valid options include 1m, 2m, 5m, 15m, 30m, 60m, 90m, and 1h.
# data = yf.download(tickers="AAPL", period="5d", interval="1m")

#fig = go.Figure(data=[go.Candlestick(x=stockdf.index,
               # open=stockdf['Open'],
                #high=stockdf['High'],
                #low=stockdf['Low'],
                #close=stockdf['Close'])])

#fig.update_layout(xaxis_rangeslider_visible=False)

# Create subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.03, row_heights=[0.7, 0.3])

# Add Candlestick
fig.add_trace(go.Candlestick(x=stockdf.index, open=stockdf['Open'], high=stockdf['High'],
                             low=stockdf['Low'], close=stockdf['Close']), row=1, col=1)

averagePrice = stockdf['Close'].mean()
fig.add_hline(y=averagePrice, line_dash="dash", line_color="blue", annotation_text=f"Average Price: ${averagePrice:.2f}", annotation_position="top left") 

# Add Volume Bar Chart
fig.add_trace(go.Bar(x=stockdf.index, y=stockdf['Volume'], name='Volume'), row=2, col=1)

fig.update_layout(xaxis_rangeslider_visible=False)

#st.markdown('### <Ticker>: <Stock/company Name>')

col1, col2 = st.columns([3, 1])

col1.markdown(f'### ${ticker}: {stock.info["longName"]}')
col1.markdown(f'### ${stockdf["Close"].iloc[-1]:.2f} ({(stockdf["Close"].iloc[-1] - stockdf["Open"].iloc[0]) / stockdf["Open"].iloc[0] * 100:.2f}%)')
col1.plotly_chart(fig, width='stretch')
col1.write("Candlestick chart for stock data, put average, volume, etc.")
col1.write("Time control for chart")

col2.markdown('#### Current Date/Time')
col2.subheader("A narrow column with the data")
col2.write("Financial info for ticker/stock")
