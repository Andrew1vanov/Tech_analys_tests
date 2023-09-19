import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import apimoex
import requests

def load_data(security: str):
    data = apimoex.get_board_history(requests.Session(), security, columns= ['CLOSE'], board = 'TQBR', 
                                     start = '2023-08-01', end = '2023-09-01')
    df = pd.DataFrame(data)
    price = df.iloc[:].values
    data2 = apimoex.get_market_history(requests.Session(), security, columns=['CLOSE'], 
                                       start = '2023-08-01', end = '2023-09-01')
    price2 = pd.DataFrame(data2).iloc[:].values
    plt.plot(price)
    #plt.plot(price2)
    plt.show()

load_data('GAZP')
load_data('LKOH')
load_data('TKS')

def guns_angels():
    print('cal')
    