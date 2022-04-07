import streamlit as st
import pandas
import base64
import matplotlib.pyplot as plt

st.markdown('''# **Crypto Price App**
A simple Cryptocurrency price from BinanceAPI''')

st.header('**Selected Price**')

dataframe = pandas.read_json('https://api.binance.com/api/v3/ticker/24hr')

def round_value(input_value):
    if input_value.values>1:
        a = float(round(input_value,2))
    else:
        a = float(round(input_value,8))
    return a

col1,col2,col3 = st.columns(3)

#Sidebar
col1_selection = st.sidebar.selectbox('Price 1',dataframe.symbol,list(dataframe.symbol).index('BTCBUSD'))
col2_selection = st.sidebar.selectbox('Price 2',dataframe.symbol,list(dataframe.symbol).index('ETHBUSD'))
col3_selection = st.sidebar.selectbox('Price 3',dataframe.symbol,list(dataframe.symbol).index('BNBBUSD'))
col4_selection = st.sidebar.selectbox('Price 4',dataframe.symbol,list(dataframe.symbol).index('XRPBUSD'))
col5_selection = st.sidebar.selectbox('Price 5',dataframe.symbol,list(dataframe.symbol).index('ADABUSD'))
col6_selection = st.sidebar.selectbox('Price 6',dataframe.symbol,list(dataframe.symbol).index('DOGEBUSD'))
col7_selection = st.sidebar.selectbox('Price 7',dataframe.symbol,list(dataframe.symbol).index('SHIBBUSD'))
col8_selection = st.sidebar.selectbox('Price 8',dataframe.symbol,list(dataframe.symbol).index('DOTBUSD'))
col9_selection = st.sidebar.selectbox('Price 9',dataframe.symbol,list(dataframe.symbol).index('MATICBUSD'))


col1_df = dataframe[dataframe.symbol==col1_selection]
col2_df = dataframe[dataframe.symbol==col2_selection]
col3_df = dataframe[dataframe.symbol==col3_selection]
col4_df = dataframe[dataframe.symbol==col4_selection]
col5_df = dataframe[dataframe.symbol==col5_selection]
col6_df = dataframe[dataframe.symbol==col6_selection]
col7_df = dataframe[dataframe.symbol==col7_selection]
col8_df = dataframe[dataframe.symbol==col9_selection]
col9_df = dataframe[dataframe.symbol==col8_selection]

col1_price = round_value(col1_df.weightedAvgPrice)
col2_price = round_value(col2_df.weightedAvgPrice)
col3_price = round_value(col3_df.weightedAvgPrice)
col4_price = round_value(col4_df.weightedAvgPrice)
col5_price = round_value(col5_df.weightedAvgPrice)
col6_price = round_value(col6_df.weightedAvgPrice)
col7_price = round_value(col7_df.weightedAvgPrice)
col8_price = round_value(col8_df.weightedAvgPrice)
col9_price = round_value(col9_df.weightedAvgPrice)


col1_percent = f'{float(col1_df.priceChangePercent)}%'
col2_percent = f'{float(col2_df.priceChangePercent)}%'
col3_percent = f'{float(col3_df.priceChangePercent)}%'
col4_percent = f'{float(col4_df.priceChangePercent)}%'
col5_percent = f'{float(col5_df.priceChangePercent)}%'
col6_percent = f'{float(col6_df.priceChangePercent)}%'
col7_percent = f'{float(col7_df.priceChangePercent)}%'
col8_percent = f'{float(col8_df.priceChangePercent)}%'
col9_percent = f'{float(col9_df.priceChangePercent)}%'

col1.metric(col1_selection,col1_price,col1_percent)
col2.metric(col2_selection,col2_price,col2_percent)
col3.metric(col3_selection,col3_price,col3_percent)
col1.metric(col4_selection,col4_price,col4_percent)
col2.metric(col5_selection,col5_price,col5_percent)
col3.metric(col6_selection,col6_price,col6_percent)
col1.metric(col7_selection,col7_price,col7_percent)
col2.metric(col8_selection,col8_price,col8_percent)
col3.metric(col9_selection,col9_price,col9_percent)

st.header('**All Price**')
st.dataframe(dataframe)

