import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import apimoex
import requests

def load_data(security: str):
    data = apimoex.get_board_history(requests.Session(), security, columns= ['CLOSE'], board = 'TQBR', 
                                     start = '2023-08-01', end = '2023-09-01')
    price = pd.DataFrame(data).iloc[:].values

    plt.plot(price)
    plt.show()

load_data('GAZP')
load_data('LKOH')

def guns_angels():
    print('cal')
    