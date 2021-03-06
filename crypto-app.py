import streamlit as st
import datetime
import pandas
import numpy
from csv import writer
import matplotlib.pyplot as plt
from binance import Client

st.markdown('''# **Crypto Price App**
A simple Cryptocurrency price from BinanceAPI 
by Tanarak Chuns 6106332 
for CSC490 Rangsit University''')

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
client = Client(st.secrets.Public_key,st.secrets.Private_key)
# client = Client(binance_key.Public_key,binance_key.Private_key)
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

count = []
HighCount = []
LowCount = []
VolCount = []
time = []
now = datetime.datetime.now()
for i in range(len(data.index)):
    
    now = now - datetime.timedelta(minutes=1)
    time.append(now.strftime("%H:%M"))
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

posUp = (HighCount.count(HighCount[-1])/120)*(LowCount.count(LowCount[-1])/120)*(count.count(count[-1])/120)
st.header('**Prediction**')
time.reverse()

def checkUpDown(preditc):
    nextUp = ''
    if preditc<=0.5:
        if count[-1] == 'Up':
            nextUp = 'Down'
        
        elif count[-1] == 'Down':
            nextUp = 'Up'
        preditc = 1-preditc
    else : 
        nextUp = count[-1]   
    return nextUp,preditc

pop,pop_percentage = checkUpDown(posUp)
print(posUp,count[-1])
st.markdown('Propablity of Price '+ pop +" {0:.2%}".format(pop_percentage))
result = data['Open'].iloc[-1] - data['Open'].iloc[-2]
print('result'+ str(result))

st.markdown('Table')
naiveTable = {'Time':time,'High':HighCount,'Low':LowCount,'Value':VolCount,'Next Price':count,'Price':data['Open']}
st.dataframe(pandas.DataFrame(data=naiveTable))
st.markdown('''Higher = Higher than average.
                Lower = Lower than average
                Up = Price Up
                Down = Price Down''')

predicted_list  = [graph_select,datetime.datetime.now(),pop,numpy.sign(result)]
with open('predicted.csv', 'a') as p_object:
    writer_object = writer(p_object)
    writer_object.writerow(predicted_list)
    p_object.close()

predicted_df = pandas.read_csv ('predicted.csv')
print(predicted_df)