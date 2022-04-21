import streamlit as st
import pandas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from binance import Client
import binance_key

st.markdown('''# **Crypto Price App**
A simple Cryptocurrency price from BinanceAPI by Tanarak Chuns''')

st.header('**Selected Price**')
dataframe = pandas.read_json('https://api.binance.com/api/v3/ticker/24hr')
def round_value(input_value):
    if input_value.values>1:
        a = float(round(input_value,2))
    else:
        a = float(round(input_value,8))
    return a

col1,col2,col3 = st.columns(3)
symbolPleaceholder = ['BTCUSDT','ETHBUSD','BNBBUSD','XRPBUSD','XRPBUSD','ADABUSD','DOGEBUSD','SHIBBUSD','DOTBUSD','MATICBUSD']
for i in range(9):
    priceHead = 'Price '+str(i+1)
    col_selection = st.sidebar.selectbox(priceHead,dataframe.symbol,list(dataframe.symbol).index(symbolPleaceholder[i]))
    col_df = dataframe[dataframe.symbol==col_selection]
    col_price = round_value(col_df.weightedAvgPrice)
    col_percent = f'{float(col_df.priceChangePercent)}%'
    if i<3:
        col1.metric(col_selection,col_price,col_percent)
    elif i>3 and i<7:
        col2.metric(col_selection,col_price,col_percent)
    else :
        col3.metric(col_selection,col_price,col_percent)

st.header('**All Price**')
st.dataframe(dataframe)

st.header('**Graph**')
plt.style.use('seaborn-bright')
client = Client(binance_key.Public_key,binance_key.Private_key)
graph_select = st.selectbox('Graph',dataframe.symbol,list(dataframe.symbol).index('BTCBUSD'))
def getminutedata(symbol,interval,lookback):
    frame = pandas.DataFrame(client.get_historical_klines(symbol,interval,lookback))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time','Open','High','Low','Close','Volume']
    frame = frame.set_index('Time')
    frame = frame.astype(float)
    return frame
data = getminutedata(graph_select,'1m','120m')
plt.cla()
plt.plot(data.index,data.Close)
plt.xlabel('Time')
plt.ylabel('Price')
plt.tight_layout()
st.pyplot(plt)



def naivebay():
    count = []
    HighCount = []
    LowCount = []
    VolCount = []
    for i in range(120):
        if data['High'].iloc[i] < data['High'].mean():
            HighCount.append('Lower')
        else: 
            HighCount.append('Higher')

        if data['Low'].iloc[i] < data['Low'].mean():
            LowCount.append('Lower')
        else: 
            LowCount.append('Higher')
        if data['Volume'].iloc[i] < data['Volume'].mean():
            VolCount.append('Lower')
        else: 
            VolCount.append('Higher')

        if data['Open'].iloc[i] < data['Close'].iloc[i] :
            count.append('Down')
        else: 
            count.append('Up')
        
    posUp = (HighCount.count(HighCount[-1])/120)*(LowCount.count(LowCount[-1])/120)*(count.count('Up')/120)
    st.header('**Prediction**')
    st.markdown('Price Up '+"{0:.3%}".format(posUp))
    st.markdown('Price Down '+"{0:.3%}".format(1-posUp))

    st.markdown('Table')
    naiveTable = {'High':HighCount,'Low':LowCount,'Value':VolCount,'Nex Price':count}
    st.dataframe(pandas.DataFrame(data=naiveTable))
    st.markdown('''Higher = Higher than average.
                    Lower = Lower than average
                    Up = Price Up
                    Down = Price Down''')
    


naivebay()

