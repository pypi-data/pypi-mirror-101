import os, platform
try:
    import pandas as pd
except:
    raise Exception("read excel need pandas")
import numpy as np

class read_data:
    
    def __init__(self, filepath, sheet=None):
        self.filepath = filepath
        self.df = None
        self.sheet = None
        self.read_data()
    
    @property
    def ext(self):
        return os.path.splitext(self.filepath)[-1]
    
    def read_data(self):
        if self.ext in ['.xlsx', '.xls']:
            if self.sheet:
                _df = pd.read_excel(self.filepath, sheet_name=self.sheet)
            _df = pd.read_excel(self.filepath)
            df = pd.DataFrame(_df.iloc[:, 1:], columns=_df.columns[1:])
            df.index = _df.iloc[:, 0]
        elif self.ext in ['.txt', '.csv']:
            if platform.system() == "Windows":
                system_line_spliter = "\n"
            else:
                system_line_spliter = "\r\n"
            if self.ext == ".txt":
                spliter = "\t"
            else:
                spliter = ","
            with open(self.filepath, "r") as f:
                if f.readable():
                    row_list = []
                    for index, line in enumerate(f.readlines()):
                        row = [cell for cell in line.split(system_line_spliter)[0].split(spliter)]
                        if index == 0:
                            columns = row
                        else:
                            row_list.append(row)
                    row_array = np.array(row_list)
                    df = pd.DataFrame(row_array[:,1:], columns=columns[1:])
                    df.index = row_array[:,0]
                else:
                    raise Exception("Unreadable file: {self.filepath}")
        else:
            raise Exception("need xlsx, xls, txt or csv")
        self.df = df
    
    def __call__(self):
        return self.df
    
    def _can_apply_type_mask(self, series, _type=float):
        try:
            series.apply(_type)
            return True
        except:
            return False
    
    @property
    def float_cols(self):
        return self.df.apply(self._can_apply_type_mask).values

def create_data(path, del_na=True, del_corr=True, return_type="ntd", del_list=[], retain_list_pre=[]):
    if isinstance(path, str):
        dataset = read_data(path)()
    else:
        import pandas as pd
        if isinstance(path, pd.DataFrame):
            dataset = path
    if len(retain_list_pre) > 0:
        retain_df = dataset.loc[:, retain_list_pre]
    if len(del_list) > 0:
        for i in del_list:
            dataset.pop(i)
    columns = dataset.columns[1:]
    indexes = dataset.index
    X = dataset.iloc[:, 1:].values
    Y = dataset.iloc[:, 0].values
    if del_na:
        from preprocessing import del_na_sd_mask
        mask = del_na_sd_mask(X)
        X = X[:, mask]
        columns = columns[mask]
    if del_corr:
        from preprocessing import del_corr_mask
        mask = del_corr_mask(X, 0.95)
        X = X[:, mask]
        columns = columns[mask]
    if len(retain_list_pre) > 0:
        intersection_list = set(retain_list_pre).intersection(set(columns))
        difference_list = set(retain_list_pre).difference(intersection_list)
        difference_df = retain_df.loc[:, difference_list]
    if return_type == "ntd":
        from collections import namedtuple
        if len(retain_list_pre) > 0:
            X = np.concatenate([X, difference_df.values], axis=1)
            columns = columns + difference_df.columns
        data = namedtuple("Data", "X, Y, columns, indexes")(*[X, Y, columns, indexes])
    elif return_type == "df":
        import pandas as pd
        data = np.concatenate([Y.reshape(-1, 1), X], axis=1)
        data = pd.DataFrame(data, columns=["target"]+list(columns), index=indexes)
        if len(retain_list_pre) > 0: data = pd.concat([data, difference_df], axis=1) 
    return data
