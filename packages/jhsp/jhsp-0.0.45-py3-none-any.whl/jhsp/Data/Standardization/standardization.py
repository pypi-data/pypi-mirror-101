import pandas as pd

class StandardizeSym():
    def __init__(self,config_path):
        self.config = {}
        data = pd.read_excel(config_path,header=0)
        for row in range(data.shape[0]):
            self.config[data.loc[row,'原症状']] = data.loc[row,'标准化症状']

    def StandardizeSyms(self,syms_list):
        config = self.config.copy()
        fail_syms = set(syms_list) - set(config.keys())

        if fail_syms:
            for i in fail_syms:
                config[i] = i

        standardize_syms_list = [config[sym] for sym in syms_list]
        return standardize_syms_list,list(fail_syms)

class StandardizeDiags():
    pass