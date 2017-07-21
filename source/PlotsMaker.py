import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy
from collections import Counter
import operator
import pandas as pd


def plot_dates(datesList, path): 
    x, y = zip(*sorted(Counter(datesList).items(),key = operator.itemgetter(0),reverse = True))
    plt.style.use('seaborn-colorblind')
    plt.style.use('seaborn-ticks')
    
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 12
    plt.gcf().autofmt_xdate()
    
    ax = plt.subplot(111)    
        
    plt.tick_params(axis="x", which="major", bottom="off", top="off",    
               labelbottom="off", left="off", right="off", labelleft="off") 
    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()  

    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)   
    
    plt.gca().yaxis.grid(True)
    
    plt.plot(x, y, marker='.', lw=2)
    d = scipy.zeros(len(y))
    ax.fill_between(x, y, where=y>=d, interpolate=True, alpha=.3)
    
    plt.ylim(0)
    myFmt = mdates.DateFormatter('%d/%m')
    ax.xaxis.set_major_formatter(myFmt)
    
    plt.show()
    plt.savefig(path+".png")
    
def test(path):
    x = pd.date_range(start = '20170101',freq='D', periods=15)
    y = [i+random.gauss(0,1) for i,_ in enumerate(x)]
    plot_datetime(dict(zip(x, y)), "path")