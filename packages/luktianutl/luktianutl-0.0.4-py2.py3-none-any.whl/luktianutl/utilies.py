import numpy as np
from collections import Iterable

def split_range(_range, split_number):
    
    step = int(np.ceil(  len(list(_range)) / split_number  ))
    
    for i in range(0, len(_range), step):
        yield _range[i:i+step]

def split_array(_array, split_number):
    
    step = int(np.ceil(  _array.shape[0] / split_number  ))
    
    for i in range(0, _array.shape[0], step):
        yield _array[i:i+step, :]

def split_param_dict(params, processornumber):
    

    for i,j in params.items():
        
        if isinstance(j, Iterable):
            
            params[i] = list(split_range(j, processornumber))
            
    
    params_list = []
    
    for i in range(processornumber):
        
        param = {}
        
        for k,v in params.items():
            
            if isinstance(v, Iterable):
                param.update(
                    {k:v[i]}
                    )
            else:
                param.update(
                    {k:v}
                    )
        params_list.append(param)
    return params_list

def split_param_dict_2(params, processornumber):
    
    for i,j in params.items():
    
        if isinstance(j, Iterable) and len(j) > processornumber:
            
            split_param_key = i
            
            split_param_values = list(split_range(j, processornumber))
            
            params.pop(i)
            
            break
        

    params_list = []
    
    for i in range(processornumber):
        
        param = {}
        
        param.update({split_param_key:split_param_values[i]})
        
        param.update(params)
        
        
        params_list.append(param)
    return params_list

def linspace(start, end, step, dtype=float, decimal=None):
    
    data = []
    while start < end:
        start = dtype(start)
        if dtype is float and decimal is not None:
            start = round(start, decimal)
        data.append(start)
        start += step
    
    return data