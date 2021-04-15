from playsound import playsound
import keyboard
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime
import time


def sound():
    # What song you want to play when BTC increases.
    playsound('')  # add the name of the mp3 file here


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
params = {
    'start': '1',
    'limit': '2',  # How many coin do you want to get data from
    'convert': 'USD'  # What currensie you want
}
headers = {
    'Accepts': 'application/json',
    # Put you API key here from coinmarketcap.com
    'X-CMC_PRO_API_KEY': '',
}

# Sends a API request to coinmarketcap.com and find right data for BTC to return in a json


def ApiRequest():
    try:
        json = requests.get(url, params=params, headers=headers).json()
        coins = json['data']
        for x in coins:
            if(x['symbol'] == 'BTC'):
                #print(x['symbol']+':', round(x['quote']['USD']['price'], 4))
                btc = x
        return btc
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

# Take the json and find BTC value in $ and the time


def BtcData():
    data = []
    Time = []
    coins = ApiRequest()
    coinvalue = round(coins['quote']['USD']['price'], 4)
    data.append(coinvalue)
    txt = coins['quote']['USD']['last_updated']
    Time = []
    thislist = txt.split("T")
    for x in thislist:
        secondlist = x.split('.')
        for y in secondlist:
            Time.append(y)
    data.append(Time[1])
    return data

# If you want to use your timezone instead of coinmarketcap's time.
# -----------------------
#x = datetime.datetime.now()
#firstTime = x.strftime("%X")


# Save the data into two variables
data = BtcData()
firstTime = str(data[1])
firstvalue = str(data[0])


time.sleep(30)
esc = False
count = 0
while (True):
    count = count + 1
    esc = keyboard.is_pressed('esc')
    if (esc == False):
        Data = BtcData()
        secondvalue = str(Data[0])
        secondTime = str(Data[1])

        # print("FirstTime: ", firstTime)
        # print("Firstvalue: $", firstvalue)
        # print("SecondTime: ", secondTime)
        # print("Secondvalue: $", secondvalue)

        # Prints outs the values
        print(firstTime + " : $" + firstvalue)
        print(secondTime + " : $" + secondvalue)

        # Checks if the BTC value have increased
        if (firstTime < secondTime and firstvalue <= secondvalue):
            diffvalue = float(secondvalue) - float(firstvalue)
            print(f"Bitcoin value has increased by ${diffvalue}")
            sound()  # Plays a song when the BTC increases. Artist/song is: Napalm Death / You Suffer
            firstTime = secondTime
            firstvalue = secondvalue
        else:
            print("The Bitcoin value is the same or it drops!")
            firstTime = secondTime
            firstvalue = secondvalue
    else:
        print("The Escape button was pressed!")
        break

# To stop the while loop after a certain time.
    if (count == 2):
        break
    time.sleep(30)
