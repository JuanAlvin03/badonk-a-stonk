import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots

def fetch_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    stockdf = stock.history(period=period, interval=interval)
    return stockdf, stock

def create_plot(stockdf):
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
    return fig

def display_main_content(stock, stockdf, ticker, fig):
    st.markdown(f'### ${ticker}: {stock.info["longName"]}')
    st.markdown(f'### ${stockdf["Close"].iloc[-1]:.2f} ({(stockdf["Close"].iloc[-1] - stockdf["Open"].iloc[0]) / stockdf["Open"].iloc[0] * 100:.2f}%)')
    st.plotly_chart(fig, width='stretch')
    st.write("Time control for chart")

def display_sidebar(stock):
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

def main():
    #==================================================================
    # Page Configurations
    #==================================================================

    st.set_page_config(layout="wide")

    #==================================================================
    # User Input
    #==================================================================

    ticker = st.text_input("Enter Ticker Symbol", value='AAPL')

    # Period and Interval Selection
    st.subheader("Period and Interval")
    
    periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', 'max']
    intervals_by_period = {
        '1d': ['15m', '1h', '1d'],
        '5d': ['15m', '1h', '1d'],
        '1mo': ['1h', '1d', '1wk'],
        '3mo': ['1d', '1wk', '1mo'],
        '6mo': ['1d', '1wk', '1mo'],
        '1y': ['1d', '1wk', '1mo'],
        '5y': ['1d', '1wk', '1mo'],
        'max': ['1d', '1wk', '1mo']
    }

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Period:**")
        selected_period = st.radio("Select Period:", periods, horizontal=True, key='period')
    
    with col2:
        st.write("**Interval:**")
        available_intervals = intervals_by_period[selected_period]
        selected_interval = st.radio("Select Interval:", available_intervals, horizontal=True, key='interval')

    #==================================================================
    # Data Fetching
    #==================================================================

    stockdf, stock = fetch_data(ticker, selected_period, selected_interval)

    #==================================================================
    # Plot Creation
    #==================================================================

    fig = create_plot(stockdf)

    #==================================================================
    # Layout
    #==================================================================

    col1, col2 = st.columns([6, 2])

    with col1:
        display_main_content(stock, stockdf, ticker, fig)

    with col2:
        display_sidebar(stock)

    with st.expander("About the Company"):
        st.write(stock.info['longBusinessSummary'])

if __name__ == "__main__":
    main()