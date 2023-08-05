import streamlit as st
import numpy as np
import pandas as pd
import time
import datetime
import pretty_errors
from tqdm import tqdm
from tqdm import trange
import random
import sys
import os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..chart.svg_charts import svg_charts
    from .GetData import StockData
    from .GetData import HolidayStockData
    from ..log.SlyLog import slog
    from ..log.SlyLog import sprint
except:
    from chart.svg_charts import svg_charts
    from GetData import StockData
    from GetData import HolidayStockData
    from log.SlyLog import slog
    from log.SlyLog import sprint



st.title('Suluoya Stock')

def get_stock_data():
    global StockData
    stock_list = st.text_area('stock', '隆基股份\n贵州茅台')
    stock_list = stock_list.split('\n')
    start_date = str(st.date_input(
        'start date',
        datetime.date(2019, 11, 1)))
    end_date = str(st.date_input(
        'end date',
        datetime.date(2020, 12, 31)))
    frequency = st.selectbox('frequency', ['d', 'w', 'm'])
    #work = st.button('Start working!')
    #if work:
    StockData=StockData(names=stock_list,
                        start_date=start_date,
                        end_date=end_date,
                        frequency=frequency)
    codes, stock_pair, stock_data = StockData.stock_data
    StockData.quit()
    for i,j in stock_pair.items():
        i,":",j
    stock_data
    
    #show_chart = st.button('show charts')
    #if show_chart:
    #stock_name=st.selectbox('stock', stock_list)
    data=[]
    for date in stock_data['date']:
        close=stock_data[stock_data['date']==date]['close']
        data.append(list(close))
    line_chart=st.line_chart(pd.DataFrame(data,columns=stock_list))
get_stock_data()