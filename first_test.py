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
        axs[0].plot([x, x + 3*x], [y, y + (-1)**mx * 3*x * i], 
                linestyle = '--', 
                c = 'orange', 
                #label = '%.2f' % i,
                alpha = 0.7)

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
    plt.fill_between(np.arange(len(sma)), U_L[0], U_L[1], alpha = 0.4, color = 'yellow')

def d_macd(sct):
    MACD = d_ema(sct, n = 12) - d_ema(sct, n = 26)
    SIGNAL = d_ema(MACD, n = 9)
    return MACD, SIGNAL

def d_rsi(sct, n = 14):
    RSI = []
    for i in range(n+1, len(sct)):
        g = sct[i-n:i] - sct[i-n-1:i-1]
        U = np.mean(g[np.where(g > 0)[0]])
        D = abs(np.mean(g[np.where(g < 0)[0]]))
        RSI.append(100 - (100/(1 + U/D)))
    RSI = np.asarray(RSI)
    return RSI



#Вычисление функций 
y, vol = load_data('YNDX') #TCSG, GAZP, LKOH, YNDX, ROSN, BSPB, SBER, VTBR
x = np.arange(len(y))

fg = plt.figure()
gs = fg.add_gridspec(3, hspace = 0, 
                    right = 0.99,
                    top = 0.99, 
                    left = 0.08, 
                    bottom = 0.08, 
                    height_ratios = [4, 1, 1])
axs = gs.subplots(sharex = True, sharey = False)


sma = d_sma(y, 55)
wma = d_wma(y, vol)
ema20 = d_ema(y)
ema100 = d_ema(y, n = 99)
ema200 = d_ema(y, n = 199)

y_min = min(y[1000:])
x_min = x[np.where(y == y_min)[0][0]]

y_max = max(y[500:])
x_max = x[np.where(y == y_max)[0][0]]



axs[0].plot(x, y, c = 'blue')

gun_angels(x_min, y_min)
#gun_angels(x_max, y_max, mx = True)

axs[0].plot(x, sma, c = 'orange', label = 'SMA',  alpha= 0.6)
axs[0].plot(x, wma, label = 'WMA', c = 'brown')
axs[0].plot(x, ema20, c = 'red', alpha= 0.5, label = 'EMA20')
axs[0].plot(x, ema100, c = 'red', alpha= 0.6, label = 'EMA100')
axs[0].plot(x, ema200, c = 'red', alpha= 0.7, label = 'EMA200')

axs[0].axis((0, max(x) * 1.05, 0, 1.1 * max(y)))#На вход получает кортеж
axs[0].grid()
axs[0].legend()
#axs[0].set_facecolor('black')

#d_Bollinger_Bands(sma)

#Построение RSI
rsi = d_rsi(y)

x_rsi = np.arange(len(rsi)) + (len(x) - len(rsi))
axs[1].plot(x_rsi, rsi, c = 'black', label = 'RSI')
axs[1].fill_between(x, np.array([70 for i in range(len(x))]),
                    np.array([30 for i in range(len(x))]),
                    color = 'purple', alpha = 0.3
                    )
#axs[1].plot(x, , '--', c = 'purple')
axs[1].axis((0, max(x) * 1.05, 0, 100))
axs[1].grid()
axs[1].legend()

#Построение MACD
macd, sign = d_macd(y)

#axs[2].bar(x, macd)
axs[2].plot(x, sign, c = 'black', label = 'MACD')
axs[2].axis((0, max(x) * 1.05, 1.1 * min(sign), 1.1 * max(sign)))
axs[2].grid()
axs[2].legend()

for ax in axs:
    ax.label_outer()

plt.show()

#testing_again