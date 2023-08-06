
import numpy as np
import math

def _counters(target):

    """
    
    counts
    
    ndarray

    index0: number or identification

    index1: target

    """
    from collections import Counter
    number_counter = Counter(target[:, 0])
    
    index_counter = {}
    
    for key, value in number_counter.items():
        value_indexes = np.where(target[:, 0] == key)[0].tolist()
        
        index_counter[key] = value_indexes
    
    value_counter = {}
    
    for key, indexes in index_counter.items():
        
        values = target[indexes, 1]
        
        values = values.astype("float")
        
        values = values.tolist()
        
        value_counter[key] = values
    
    return index_counter, value_counter

def _get_gap(_list):
    
    gap_list = []
    
    for i, j in zip(_list[1:], _list[:-1]):
        
        gap_list.append(float(i) - float(j))
    
    return gap_list

def _prone_list_target_mean(target_list, criterion):
    """
    target_list: list
    """
    
    target_list.sort()
    while np.std(target_list) > criterion and len(target_list) > 2:
        
        gap_list = _get_gap(target_list)
        
        popindex = gap_list.index(max(gap_list))
        
        if popindex >= math.floor(len(target_list) / 2):
            popindex += 1
        
        target_list.pop(popindex)
    
    
    return np.mean(target_list)

def deal_with_multiple_data(target, deal="mean"):
    """
    
    transfer
    
    ndarray

    index0: number or identification

    index1: target

    deal: mean, max, min, prone_mean

    """
    
    index_counter, value_counter = _counters(target)
    
    counters = dict(
        index_counter=index_counter,
        value_counter=value_counter
        )
    
    data = []
    
    for key, values in value_counter.items():
        
        if deal == "mean":
            value = np.mean(values)
        elif deal == "max":
            value = np.max(values)
        elif deal == "min":
            value = np.min(values)
        elif deal == "prone_mean":
            value = _prone_list_target_mean(values, criterion=0.01)
        
        data.append([key, value])
    
    data = np.array(data)
    
    return data, counters


def reg2cls(Y, class_number=2, deal="median"):
    
    try:
        Y = Y.reshape(-1, )
        Y = Y.astype(float)
    except Exception as err:
        return err
    
    try:
        class_number = int(class_number)
    except Exception as err:
        return err
    
    if class_number == 2:
        if deal == "median":
            deal = np.median(Y)
        elif deal == "mean":
            deal = np.mean(Y)
        for i, value in enumerate(Y):
            if value >= deal:
                Y[i] = 1
            else:
                Y[i] = 0
    elif class_number != 2:
        #ignore deal
        #split part
        step = 100 / class_number
        bins = [ [np.percentile(Y, i*step), np.percentile(Y, (i+1)*step)] for i in range(class_number) ]
        for i, value in enumerate(Y):
            for j, _bin in enumerate(bins):
                if _bin[0] <= value <= _bin[1]:
                    Y[i] = j
    return Y



if __name__ == "__main__":

    # import pandas as pd
    # from glob import glob

    # target = pd.read_csv(glob("化学式.csv")[0], encoding="gbk").to_numpy()

    # data, counters = deal_with_multiple_data(target[:, 1:], deal="prone_mean")
    # pd.DataFrame(data).to_csv("dealed_formular.csv", index=None)
    Y = np.linspace(1, 100, 50)
    Ycls = reg2cls(Y, class_number=5)