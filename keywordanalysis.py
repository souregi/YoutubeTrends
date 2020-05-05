from pytrends.request import TrendReq
from operator import itemgetter
import random
import numpy as np
import matplotlib.pyplot as plt
import time

pytrend = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def plotkeywords1H():
    plotkeywords('now 1-H')

def plotkeywords4H():
    plotkeywords('now 4-H')		

def plotkeywords24H():
    plotkeywords('now 1-d')

def plotkeywords(periodOfTime):
    with open('keywords.txt') as f:
        my_list = list(f)
        my_list = [w.replace('\n', '') for w in my_list]
    my_key = my_list[0]
    chunkList = list(chunks(my_list[1:], 4))
    for chunkElement in chunkList:
        chunkElement.extend([my_key])
        averageScorePerElementList = []
        pytrend.build_payload(kw_list=chunkElement, gprop='youtube', timeframe= periodOfTime)
        interest_over_time_df = pytrend.interest_over_time()
        if(interest_over_time_df.empty == False):
            for elmt in chunkElement:
                averageScorePerElementList.append([elmt, interest_over_time_df[elmt].mean()])
            my_key, value = max(averageScorePerElementList, key=lambda item: item[1])
    print('Most searched keyword is : ' + my_key)
    print('---------------------------------')
    my_list.remove(my_key)

    finalScoreList = []
    finalScoreList.append([my_key, 100])
    chunkList = list(chunks(my_list, 4))
    for chunkElement in chunkList:
        chunkElement.extend([my_key])
        averageScorePerElementList = []

        pytrend.build_payload(kw_list=chunkElement, gprop='youtube', timeframe= periodOfTime)
        interest_over_time_df = pytrend.interest_over_time()
        if(interest_over_time_df.empty == False):
            for elmt in chunkElement:
                averageScorePerElementList.append([elmt, interest_over_time_df[elmt].mean()])

            bestScore = 100 / averageScorePerElementList[-1:][0][1]
            for averageScore in averageScorePerElementList[:-1]:
                finalScoreList.append([averageScore[0], bestScore * averageScore[1]])


    sortedFinalScoreList = sorted(finalScoreList, key=itemgetter(1),reverse=True)
    np.arange(len([w[0] for w in sortedFinalScoreList]))
    y_pos = np.arange(len([w[0] for w in sortedFinalScoreList]))
    scores = [w[1] for w in sortedFinalScoreList]

    plt.figure(figsize=(10, len(sortedFinalScoreList) * 2))
    plt.barh(y_pos, scores, height=0.5)
    plt.yticks(y_pos, [w[0] for w in sortedFinalScoreList])
    plt.show()
