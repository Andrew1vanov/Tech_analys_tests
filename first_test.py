import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import apimoex
import requests

def load_data(security: str):
    data = apimoex.get_board_history(requests.Session(), security, 
                                    columns= ['CLOSE', 'VOLUME'],
                                    board = 'TQBR')
    price = pd.DataFrame(data)
    vol = price.fillna(price.mean()).iloc[:, 1].values.ravel()
    price = price.fillna(price.mean()).iloc[:, 0].values.ravel()
    return price, vol

def gun_angels(x, y, mx = False):
    t_ang = np.array([1/8, 1/4, 1/3, 1/2, 1, 2, 3, 4, 8])
    for i in t_ang:
        plt.plot([x, x + 3*x], [y, y + (-1)**mx * 3*x * i], 
                linestyle = '--', 
                c = 'red', 
                #label = '%.2f' % i,
                alpha = 0.35)

def d_sma(sct, n = 21):
    SMA = np.array([sum(sct[i-n:i]) / n for i in range(len(sct))])
    return SMA

def d_wma(sct, vol, n = 21):
    WMA = np.array([(sum(sct[i-n:i] * vol[i-n:i]) / sum(vol[i-n:i])) if i-n >= 0 else 0
                    for i in range(len(sct))])
    return WMA

def d_ema(sct, n = 21):
    K = 2/(n+1)
    EMA = [sct[0]]
    for i in range(len(sct)):
        EMA.append(EMA[-1] + (K * (sct[i] - EMA[-1])))
    EMA.pop(0)
    EMA = np.asarray(EMA)
    return EMA

def d_Bollinger_Bands(sma):
    U_L = np.array([[(1 + 10/100) * sma[i] for i in range(len(sma))],
                    [(1 - 10/100) * sma[i] for i in range(len(sma))]])
    plt.fill_between(np.arange(len(U_L[1])), U_L[0], U_L[1], alpha = 0.4, color = 'yellow')

def d_macd(sct):
    MACD = d_ema(sct, n = 12) - d_ema(sct, n = 26)
    SIGNAL = d_ema(MACD, n = 9)
    return MACD, SIGNAL

#Вычисление функций 
y, vol = load_data('GAZP')
x = np.arange(len(y))

sma = d_sma(y, 55)
wma = d_wma(y, vol)
ema20 = d_ema(y)
macd, sign = d_macd(y)

y_min = min(y)
x_min = x[np.where(y == y_min)[0][0]]

plt.plot(x, y, c = 'blue')

gun_angels(x_min, y_min)

plt.plot(x, sma, c = 'orange', label = 'SMA',  alpha= 0.6)
plt.plot(x, wma, label = 'WMA', c = 'brown')
plt.plot(x, ema20, c = 'green', alpha= 0.8, label = 'EMA20')
plt.plot(x, sign, c = 'black', label = 'MACD')
#plt.bar(x, macd)

#d_Bollinger_Bands(sma)

plt.axis((0, max(x) * 1.05, y_min * 0.8, 1.1 * max(y)))#На вход получает кортеж
plt.grid()
plt.legend()
plt.show()