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


def plot_dates(data, path, x_label='временной интервал', y_label='всего упоминаний', title=''):
    plt.style.use('seaborn-ticks')
    plt.style.use('seaborn-colorblind')
    _, ax = plt.subplots()
    ax.hist(data, alpha=0.75, color="#0072B2", linewidth=0.5, bins=12, edgecolor='white')
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.gca().yaxis.grid(True)
    
    plt.tick_params(axis="x", which="major", bottom="off", top="off",    
              labelbottom="off", left="off", right="off", labelleft="off") 
   
    myFmt = mdates.DateFormatter('%d/%m')
    ax.xaxis.set_major_formatter(myFmt)
    plt.gcf().autofmt_xdate()
    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()  

    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False) 

    plt.savefig(path+".png")
    
def test(path):
    data = [date(2017, random.randint(1, 12), random.randint(1, 28)) for i in range(2000)]  
    plot_dates(data, path)