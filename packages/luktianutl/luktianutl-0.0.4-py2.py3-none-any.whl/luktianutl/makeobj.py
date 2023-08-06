
default_preprocessings = dict(
    StandardScaler=dict(),
    MinMaxScaler=dict(),
    Normalizer=dict(),
    PowerTransformer=dict(),
    QuantileTransformer=dict(),
    RobustScaler=dict()
    )

default_decompositions = dict(
    DictionaryLearning=dict(),
    FactorAnalysis=dict(),
    FastICA=dict(),
    IncrementalPCA=dict(),
    KernelPCA=dict(),
    LatentDirichletAllocation=dict(),
    NMF=dict(),
    PCA=dict(),
    SparsePCA=dict()
    )

default_cluster = dict(
    AffinityPropagation=dict(),
    AgglomerativeClustering=dict(),
    Birch=dict(),
    DBSCAN=dict(),
    KMeans=dict(),
    MeanShift=dict(),
    OPTICS=dict()
    )

def make_scales(X, Y, preprocessings=None):
    """
    

    Parameters
    ----------
    X : ndarray
        DESCRIPTION.
    Y : TYPE
        DESCRIPTION.
    preprocessings : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    scaled_Xs : TYPE
        DESCRIPTION.

    """
    if preprocessings is None:
        preprocessings = default_preprocessings
    if "QuantileTransformer" in preprocessings.keys():
        preprocessings["QuantileTransformer"].update(dict(n_quantiles=X.shape[0]))
    scaler = dict(scaler=None)
    scaled_Xs = dict()
    for preprocessing, params in preprocessings.items():
        exec(f"from sklearn.preprocessing import {preprocessing}")
        exec(f"scaler['scaler'] = {preprocessing}")
        scaled_X = scaler['scaler'](**params).fit_transform(X, Y)
        scaled_Xs.update({preprocessing:scaled_X})
    return scaled_Xs

def make_models(methods=None, default="cluster"):
    """
    

    Parameters
    ----------
    methods : TYPE, optional
        DESCRIPTION. The default is None.
    default : str, cluster or decomposition
        DESCRIPTION. The default is "cluster".

    Returns
    -------
    models : TYPE
        DESCRIPTION.

    """
    if default is None:
        default = "cluster"
    if methods is None:
        if default == "cluster":
            methods = default_cluster
        elif default == "decomposition":
            methods = default_decompositions
    model = dict(model=None)
    models = dict()
    for method, params in methods.items():
        exec(f"from sklearn.{default} import {method}")
        exec(f"model['model'] = {method}")
        models.update({method: [model['model'], params]})
    return models


