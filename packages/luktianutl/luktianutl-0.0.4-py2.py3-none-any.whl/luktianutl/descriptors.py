import pickle, numpy as np, platform

if platform.system() == "Windows":
    file_dir_path = __file__.split("\\descriptors.py")[0]
    descriptorpkl_path = file_dir_path +"\\sources\\descriptors.pkl"
    descriptorxlsx_path = file_dir_path +"\\sources\\descriptors.xlsx"
    ionicradiipkl_path = file_dir_path +"\\sources\\ionicradii.pkl"
else:
    file_dir_path = __file__.split("/descriptors.py")[0]
    descriptorpkl_path = file_dir_path +"/sources/descriptors.pkl"
    descriptorxlsx_path = file_dir_path +"/sources/descriptors.xlsx"
    ionicradiipkl_path = file_dir_path +"/sources/ionicradii.pkl"

class Descriptors:
    def __init__(self):
        self.fields = None
        self.atoms = None
        self.mvdes = None
        self.ions = None
        self.load_pkl()
    
    def __getitem__(self, atom, chg=None, occu=None):
        atom_index = self.atoms.index(atom)
        des = self.mvdes[atom_index, :]
        if occu is None:
            return des * 1
        else:
            tmp = self.ions[np.where(self.ions[:, 0]==atom)]
            if chg:
                tmp = tmp[np.where(tmp[:, 1]==chg)]
            if occu:
                tmp = tmp[np.where(tmp[:, 2]==occu)]
            return np.concatenate([des, np.array(tmp[-1][-1]).reshape(1,)])
    
    @property
    def columns(self):
        return self.fields
    
    def refresh_pkl(self):
        import pandas as pd
        vdes = pd.read_excel(descriptorxlsx_path, sheet_name="v", index_col=0)
        mdes = pd.read_excel(descriptorxlsx_path, sheet_name="m", index_col=0)
        ionicradii = pd.read_excel(descriptorxlsx_path, sheet_name="mendeleev_ionicradii").iloc[:, [0, 1, 3, 7]].values
        
        mdes_col_mask = np.ones(mdes.shape[1], dtype=bool)
        for i,j in enumerate(mdes_col_mask):
            try:
                mdes.iloc[:,i].apply(float)
            except:
                mdes_col_mask[i] = False
        mdes = mdes.loc[:, mdes_col_mask]
        
        if vdes.index.all() == mdes.index.all():
            atoms = vdes.index = mdes.index
        else:
            raise Exception("indexes not equal in vdes and mdes")
        
        fields = mdes.columns.tolist()+vdes.columns.tolist()
        
        mvdes = pd.concat([mdes, vdes], axis=1)
        
        data = {
            "fields": fields,
            "atoms": atoms.tolist(),
            "mvdes": mvdes.values,
            "ions": ionicradii
            }
        with open(descriptorpkl_path, "wb") as f:
            pickle.dump(data, f)
    
    def load_pkl(self):
        with open(descriptorpkl_path, "rb") as f:
            self.descriptors_dict = pickle.load(f)
        self.fields = self.descriptors_dict["fields"]
        self.atoms = self.descriptors_dict["atoms"]
        self.mvdes = self.descriptors_dict["mvdes"]
        self.ions = self.descriptors_dict["ions"]

def self_mul(row, ratio):
    '''
    

    Parameters
    ----------
    row : array
        DESCRIPTION.
    ratio : float
        DESCRIPTION.

    Returns
    -------
    row.

    '''
    
    ratio = float(ratio)
    for index, i in enumerate(row):
        
        if isinstance(i, float):
            mul = i * ratio
        elif str(i) == "nan":
            mul = i
        elif isinstance(i, str):
            try:
                i = float(i)
                mul = i 
            except ValueError:
                mul = i
        row[index] = mul
        
    return row

def self_add(site_data, new_row):
    
    for index, i in enumerate(site_data):
        
        if str(new_row[index]) == "nan" or str(i) == "nan":
            add = np.nan
        else:
            try:
                i = float(i)
                j = float(new_row[index])
                add = j + i
            except:
                add = new_row[index]
        try:
            site_data[index] = add
        except:
            site_data[index] = i
    
    return site_data

def _gen_sites_data(formular_data, column_mask=None):
    if isinstance(formular_data[0], dict):
        formular_data = [ list(i.items()) for i in formular_data]
    des = Descriptors()
    des.show = "array"
    site_init = np.zeros(len(des.columns("vmdes")))
    sites_data = []
    for site in formular_data:
        site_data = 1 * site_init
        for ele, ratio in site:
            tmp = self_mul(des[ele], ratio)
            site_data = self_add(site_data, tmp)
        sites_data += site_data.tolist()
    sites_data = np.array(sites_data)
    if column_mask.any():
        sites_data = sites_data[column_mask]
    return sites_data

def gen_sites_data(formular_data, column_names, prefixes):
    
    des = Descriptors()
    des.show = "array"
    columns = [ ]
    for i in prefixes:
        columns += des.columns("vmdes", i) 
    column_mask = np.zeros(len(columns), dtype=bool)
    for i in column_names:
        column_mask[columns.index(i)] = True
    
    sites_data = _gen_sites_data(formular_data, column_mask)
    return sites_data

def tolerance_factor(ra, rb, rc):
    return (ra + rc) / (np.sqrt(2) * (rb + rc))

def tau_factor(na, ra, rb, rc):
    left = rc/rb
    right_denominator = np.log(ra/rb)
    right_numerator = ra/rb
    right = na * (na - right_numerator/right_denominator)
    return left - right

def octahedral_factor(rb, rc):
    return rb/rc

if __name__ == "__main__":
    # import pandas as pd
    # vdes = pd.read_excel(descriptorxlsx_path, sheet_name="v", index_col=0)
    # mdes = pd.read_excel(descriptorxlsx_path, sheet_name="m", index_col=0)
    # ionicradii = pd.read_excel(descriptorxlsx_path, sheet_name="mendeleev_ionicradii").iloc[:, [0, 1, 3, 7]].values
    
    # mdes_col_mask = np.ones(mdes.shape[1], dtype=bool)
    # for i,j in enumerate(mdes_col_mask):
    #     try:
    #         mdes.iloc[:,i].apply(float)
    #     except:
    #         mdes_col_mask[i] = False
    # mdes = mdes.loc[:, mdes_col_mask]
    
    # if vdes.index.all() == mdes.index.all():
    #     atoms = vdes.index = mdes.index
    # else:
    #     raise Exception("indexes not equal in vdes and mdes")
    
    # fields = vdes.columns.tolist()+mdes.columns.tolist()
    
    # mvdes = pd.concat([mdes, vdes], axis=1)
    
    # data = {
    #     "fields": fields,
    #     "atoms": atoms.tolist(),
    #     "mvdes": mvdes.values,
    #     "ions": ionicradii
    #     }
    # with open(descriptorpkl_path, "wb") as f:
    #     pickle.dump(data, f)

    des = Descriptors()
    des.__getitem__("H", "I")
    des.refresh_pkl()
 