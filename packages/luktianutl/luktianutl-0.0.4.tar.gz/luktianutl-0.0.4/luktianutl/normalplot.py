
import math
import matplotlib.pyplot as plt
import numpy as np

def scatterplot(X=None, color=None, title="normalplot", legend=None, annotate=None, dpi=600):
    
    plt.figure(dpi=dpi)
    plt.scatter(X[:,0], X[:,1], c=color)
    plt.title(title)
    plt.legend(legend)
    if annotate is not None:
        for index, annotate_ in enumerate(annotate):
            plt.annotate(annotate_, xy=(X[index,0], X[index,1]))
    return plt

def scatterplot_2_2(X1, X2, X3, X4, title="normalplot", legend=None, dpi=600):
    
    min_ = math.floor(min(min(X1), min(X2), min(X3), min(X4))*0.9)
    max_ = math.ceil(max(max(X1), max(X2), max(X3), max(X4))*1.1)
    
    x = np.linspace(min_, max_, 10)
    y = x
    
    
    plt.figure(dpi=dpi)
    plt.scatter(X1, X2)
    plt.scatter(X3, X4)
    plt.plot(x, y)
    plt.title(title)
    plt.legend(legend)
        
    plt.xlim(left=min_, right=max_)
    plt.ylim(bottom=min_, top=max_)
    
    return plt
