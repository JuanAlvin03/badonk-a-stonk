import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots

#==================================================================
# Page Configurations
#==================================================================

st.set_page_config(layout="wide")

#==================================================================
# Logic
#==================================================================

ticker = 'AAPL'
#stockdf = yf.download(ticker, start='2023-01-01', end='2024-01-01')
stock = yf.Ticker(ticker)
#stockdf = stock.history(period='1y')
stockdf = stock.history(period='1d', interval='15m')

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

#==================================================================
# Main Column
#==================================================================
col1, col2 = st.columns([6, 2])

with col1:
    st.markdown(f'### ${ticker}: {stock.info["longName"]}')
    st.markdown(f'### ${stockdf["Close"].iloc[-1]:.2f} ({(stockdf["Close"].iloc[-1] - stockdf["Open"].iloc[0]) / stockdf["Open"].iloc[0] * 100:.2f}%)')
    st.plotly_chart(fig, width='stretch')
    st.write("Candlestick chart for stock data, put average, volume, etc.")
    st.write("Time control for chart")

with col2:
    st.write("Date/Time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    findata = pd.DataFrame({'EPS(TTM)': [stock.info['trailingEps']], 
                            'PE Ratio(TTM)': [stock.info['trailingPE']],
                            'Market Cap': [stock.info['marketCap']],
                            'Dividend Yield': [stock.info['dividendYield']],
                            'Volume': [stock.info['volume']],
                            'Average Volume': [stock.info['averageVolume']],
                            '52 Week Low': [stock.info['fiftyTwoWeekLow']],
                            '52 Week High': [stock.info['fiftyTwoWeekHigh']]
                            })
    
    findata = findata.transpose()
    st.dataframe(findata)

    #subcol1, subcol2 = st.columns(2)

    #with subcol1:
    #    st.markdown("**EPS(TTM)**")
    #    st.markdown("{:.2f}".format(stock.info['trailingEps']))
    #with subcol2:
    #    st.markdown("**PE Ratio(TTM)**  " \
    #    "{:.2f}".format(stock.info['trailingPE']))

#==================================================================
# End of Main Column
#==================================================================

with st.expander("About the Company"):
    st.write(stock.info['longBusinessSummary'])