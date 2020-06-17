import  requests, json
from datetime import datetime
import time
import datetime

# Получить цвет свечи
def getColor(ohlc):
    if (ohlc[1] < ohlc[4]):
        return 'green'
    else:
        return 'red'

# Посчитать ряды по всем интервалам
def compute(json, profit_sequence = 5, candles_print=False):
    data = {} # Результаты r0 - x
    # Создаём заглушки с нулями в data
    max_sequence_length = 20 # Максимальное количество одноцветных свечей в ряду
    for x in range(max_sequence_length):
        i = x + 1
        data['g' + str(i)] = 0
    for x in range(max_sequence_length):
        i = x + 1
        data['r' + str(i)] = 0
    
    if(candles_print): # Напечатать свечи, если надо
        for ohlc in json:
            print(str(json.index(ohlc)+1) + getColor(ohlc))
                
    sequence = 0
    summ_profit = 0
    for j in range (max_sequence_length): # Проходим по всем рядам
        sequence = j + 1
        i = 0
        for ohlc in json: # Проверяем все свечи из переданных значений
            if ((sequence-1) > i): # Начало пропускаем до текущего интервала
                i = i + 1
            else:
                green_pattern = True
                red_pattern = True
                if (getColor(ohlc) == 'green'):
                    for x in range(sequence):
                        if (getColor(json[i-x]) != 'green'):
                            green_pattern = False
                    if (green_pattern):
                        key = 'g'+ str(sequence)
                        data[key]+=1
                        if ( (sequence == profit_sequence) and ((i+1) < len(json)) ):
                            p = computeCandleProfit(json[i+1], 'short')
                            print('SHORT ' + str(p) + '%')
                            summ_profit += p
                else:
                    for x in range(sequence):
                        if (getColor(json[i-x]) != 'red'):
                            red_pattern = False
                    if (red_pattern):
                        key = 'r'+str(sequence)
                        data[key]+=1
                        if ( (sequence == profit_sequence) and ((i+1) < len(json)) ):
                            p = computeCandleProfit(json[i+1], 'long')
                            print('LONG  ' + str(p) + '%')
                            summ_profit += p
                i = i + 1
    print('Total Profit: ' + str(summ_profit) + '%')
    return data

# Получить процент который составляет part от whole
def percentage(part, whole):
    return 100 * float(part)/float(whole)
                
# Расчитать профит свечи
def computeCandleProfit(ohlc, direction, fee=0.075): # 0.075 fee для Spot, и 0.04 fee для Futures
    if (direction == 'long'):
        return (100-percentage(ohlc[1], ohlc[4])) - (fee * 2)
    else:
        return ((100-percentage(ohlc[1], ohlc[4]))*-1) - (fee * 2)
    
    
symbol = 'BTC' + 'USDT' # Валютная пара
interval = '1m' # Таймфрейм
limit = '1000' # Количество свечей
date_form = str(time.mktime(time.strptime('2020-05-11 15:00:00', "%Y-%m-%d %H:%M:%S")))[:-2] # Опционально, если что удалить параметры из URL
date_to = str(time.mktime(time.strptime('2020-05-12 15:00:00', "%Y-%m-%d %H:%M:%S")))[:-2] # Опционально, если что удалить параметры из URL

# Binance Futures
# url = 'https://fapi.binance.com/fapi/v1/klines?symbol='+symbol+'&interval='+interval+'&limit='+limit + '&startTime=' + date_form + '000&endTime=' + date_to + '000' #https://api.binance.com/api/v3/
# Binance Spot
url = 'https://api.binance.com/api/v1/klines?symbol='+symbol+'&interval='+interval+'&limit='+limit + '&startTime=' + date_form + '000&endTime=' + date_to + '000' #https://api.binance.com/api/v3/

response = requests.get(url)
myjson = response.json()

# Количество свечей
print(str(len(myjson))) 

 # Для подсчёта профита указано открыть сделку после 12 свечи
data = compute(myjson,12)

# Печатем результат по количеству свечей и профиту
print(json.dumps(data, indent=4, sort_keys=False))
