import importlib.resources as ir
import pandas as pd


def load_data(subpkg=None, name=None, dct=None):
    """
    Load example data included in the pyrsm package

    Parameters
    ----------
    subpkg : str
        One of "data", "design", "basics", "model", or "multivariate"
        These string coincide with the dropdown menuss at https://radiant-rstats.github.io/docs/
        If None, files from all dictionaries will be returned
    name : str
        Name of the dataset you want to load (e.g., "diamonds").
        If None, all datasets will be returned
    dct : dct
        Dictionary to add datasets to. For example, using globals() will add
        dataframes to the global environment in python. If None, a dictioary
        with datasets will be returned

    Examples
    --------
    load_state(globals(), path="my-notebook.state.pkl")
    """

    pkg = "pyrsm.data"

    def load(gen):
        with gen as data_path:
            return pd.read_pickle(data_path)

    def mkdct(spkg):
        data = {}
        for sp in spkg:
            data.update(
                {
                    f.replace(".pkl", ""): load(ir.path(f"{pkg}.{sp}", f))
                    for f in ir.contents(f"{pkg}.{sp}")
                    if (name is None and f[0:2] != "__") or f == name + ".pkl"
                }
            )
        return data

    if subpkg is None:
        data = mkdct([d for d in ir.contents(pkg) if d[0:2] != "__"])
    elif name is None:
        data = mkdct([subpkg])
    elif subpkg is not None and name is not None:
        data = {name: load(ir.path(f"{pkg}.{subpkg}", name + ".pkl"))}
    else:
        data = {}

    if dct is None:
        return data
    else:
        for key, val in data.items():
            dct[key] = val
