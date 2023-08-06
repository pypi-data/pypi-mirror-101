
def lib():
    string = "import pandas as pd\
    import numpy as np\
    from xgboost import XGBRegressor\
    import pickle, random, os\
    from preprocessing import del_na_sd_mask, del_corr_mask\
    from validates import validate_switch, validate_from_trees, validate_switch_from_trees\
    from sphere_exclusion import perm_rng\
    from normalplot import scatterplot_2_2\
    from imports import lib\
    "
    return string