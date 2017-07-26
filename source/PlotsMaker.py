from datetime import date
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy
from collections import Counter
import operator
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator

def plot_dates(data, path):
    plt.gca().yaxis.grid(True)
    plt.style.use('seaborn-ticks')
    plt.style.use('seaborn-colorblind')
    plt.style.use('seaborn-ticks')
    
    ax = plt.subplot(111)  
    plt.tick_params(axis="x", which="both", bottom="off", top="off",    
                   labelbottom="off", left="off", right="off", labelleft="off") 
    ax.set_ylabel('всего упоминаний')
    ax.set_xlabel('временной интервал')
    ax.yaxis.set_ticks_position('none')  

    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()  

    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)   

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    if len(Counter(data)) > 2:
        data = [d for d in data if d.year > 2015]
        ax.hist(data, alpha=0.75, color="#0072B2", linewidth=0.5, bins=12, edgecolor='white')  
    else:
        c = dict(Counter(data))  
        l = sorted(c.keys())  
        x, y = zip(*sorted(Counter(data).items(), key = operator.itemgetter(0),reverse = True))

        base = l[0]
        x = [base+datetime.timedelta(days=x) for x in range(-5, (l[-1:][0] - base).days+5)]
        y = [c[x1] if x1 in c else 0 for x1 in x]
        maxy = max(y)
        plt.ylim(0, maxy+1)
        plt.bar(x, y, linewidth=1, color="#0072B2",edgecolor="#0072B2", alpha=0.75)
    
    myFmt = mdates.DateFormatter('%d/%m/%Y')
    ax.xaxis.set_major_formatter(myFmt)
    plt.gcf().autofmt_xdate()
    plt.savefig(path+".png")
    plt.close('all')
    
def test(path, data=None):
    if data == None:
        data = [date(2017, random.randint(1, 12), random.randint(1, 28)) for i in range(2000)]  
    plot_dates(data, path)