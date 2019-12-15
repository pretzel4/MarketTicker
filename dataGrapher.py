import json
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np    
import matplotlib.lines as mlines
from os import listdir
import os
import time
from os.path import isfile, join
import CMethods
import shutil
print("Starting!")
algoNumber = 1
INPUT_PATH = "./data/BTC-BAT"
OUTPUT_PATH = "./CMData/BTC-BAT"
CANDLE_PATH = "./ETH-NEOcandles.json"
onlyfiles = [f for f in sorted(listdir(INPUT_PATH)) if isfile(join(INPUT_PATH, f))]
counter = 0

#Cleaning files
"""if(os.path.exists(OUTPUT_PATH)):
    shutil.rmtree(OUTPUT_PATH)
os.mkdir(OUTPUT_PATH)
for i in onlyfiles:
    CMethods.findAddressChanges((INPUT_PATH + "/" + i).encode(), (OUTPUT_PATH + "/" + i).encode(), CANDLE_PATH.encode(), algoNumber)
    print("Compiling data: " + str((counter / len(onlyfiles)) * 100))
    counter += 1"""

counter = 0
#Plotting the candles
candles = {}

with open(CANDLE_PATH) as json_file:
    candles = json.load(json_file)
    json_file.close()

def splitXandY(points, xLabel, yLabel):
    xArray = []
    yArray = []
    for i in points:
        xArray.append(i[xLabel])
        yArray.append(i[yLabel])
    return {'x':xArray, 'y': yArray}

for i in candles["result"]:
    unixtime = time.mktime(time.strptime(i['T'], '%Y-%m-%dT%H:%M:%S'))
    
    i['TM'] = float(unixtime)
    i['C'] = float(i['C'])
    print("Plotting candles: " + str((counter / len(candles["result"])) * 100))
    counter += 1

coordinateData = splitXandY(candles['result'], 'TM', 'C')
plt.plot(coordinateData['x'], coordinateData['y'])

counter = 0
outfiles = [f for f in sorted(listdir(OUTPUT_PATH)) if isfile(join(OUTPUT_PATH, f))]

def convertRGBtoHex(r,g,b):
    if(r > 255):
        r = 255
    elif(r < 0):
        r = 0
    if(g > 255):
        g = 255
    elif(g < 0):
        g = 0
    if(b > 255):
        b = 255
    elif(b < 0):
        b = 0
    return '#%02x%02x%02x' % (r,g,b)

def algo0(data):
    for b in data['book']['data']['SELL']:
        plt.scatter(float(data['book']['timestamp']), b["P"], c="red")
    for b in data['book']['data']['BUY']:       
        plt.scatter(float(data['book']['timestamp']), b["P"], c="green")

def algo1(data):
    orderList = data['book']['data']['SELL']
    #SELL DATA
    if(len(orderList) != 0 and len(orderList) != 1):
        minQ = float(orderList[0]['Q'])
        maxQ = float(orderList[len(orderList) - 1]['Q'])
        Qrange = maxQ - minQ
        for b in data['book']['data']['BUY']:
            newRange = maxQ - b['Q']
            colorPercent = newRange/Qrange
            newColor = convertRGBtoHex(255, 0, 0)
            alphaValue = colorPercent
            if(alphaValue > 1.0):
                alphaValue = 1.0
            elif(alphaValue < 0.0):
                alphaValue = 0.0
            plt.scatter(float(data['book']['timestamp']), b["R"], c=newColor, alpha=alphaValue)
    else:
        for b in data['book']['data']['BUY']:
            plt.scatter(float(data['book']['timestamp']), b["R"], c="blue")
    #BUY DATA
    orderList = data['book']['data']['BUY']
    if(len(orderList) != 0 and len(orderList) != 1):
        minQ = float(orderList[0]['Q'])
        maxQ = float(orderList[len(orderList) - 1]['Q'])
        Qrange = maxQ - minQ
        for b in data['book']['data']['BUY']:
            newRange = maxQ - b['Q']
            colorPercent = newRange/Qrange
            newColor = convertRGBtoHex(0, 255, 0)
            alphaValue = colorPercent
            if(alphaValue > 1.0):
                alphaValue = 1.0
            elif(alphaValue < 0.0):
                alphaValue = 0.0
            plt.scatter(float(data['book']['timestamp']), b["R"], c=newColor, alpha=alphaValue)
    else:
        for b in data['book']['data']['BUY']:
            plt.scatter(float(data['book']['timestamp']), b["R"], c="blue")

def algo2(data):
    for b in data['book']['data']['SELL']:
        plt.scatter(float(data['book']['timestamp']), b["R"], c="red")
    for b in data['book']['data']['BUY']:       
        plt.scatter(float(data['book']['timestamp']), b["R"], c="green")


for i in outfiles:
    if(counter % 250 == 0):
        json_file = None
        with open(OUTPUT_PATH + "/" + i) as json_file:
            data2 = json.load(json_file)
            if(algoNumber == 0):
                algo0(data2)
            elif(algoNumber == 1):
                algo1(data2)
            elif(algoNumber == 2):
                algo2(data2)
            json_file.close()
    print("Plotting dots: " + str((counter / len(outfiles)) * 100))
    counter += 1
            


plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
#https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=BTC-XMR&tickInterval=onemin&_=1499127220008