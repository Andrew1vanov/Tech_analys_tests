import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import apimoex
import requests
import math

def load_data(security: str):
    data = apimoex.get_board_history(requests.Session(), security, 
                                    columns= ['CLOSE'],
                                    board = 'TQBR')
    price = pd.DataFrame(data).iloc[:].values
    return price

def gun_angels():
    y = load_data('GAZP')
    x = np.arange(len(y))
    y_min = min(y)
    x_min = x[(np.where(y == y_min))[0][0]]

    t_ang = np.array([1/8, 1/4, 1/3, 1/2, 1, 2, 3, 4, 8])
    y_graf = np.array([len(y) * i for i in t_ang])
    print(y_graf)

    for i in range(len(y_graf)):
        plt.plot([0, len(y)], [0, y_graf[i]])
    plt.ylim(0, 2000)
    plt.show()

gun_angels()
