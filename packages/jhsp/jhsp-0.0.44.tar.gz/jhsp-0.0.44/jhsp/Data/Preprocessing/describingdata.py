import pandas as pd
import os
import sys

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

class DescribingData:
    def __init__(self, old_dir):
        self.data = self.data = pd.read_excel(old_dir, header=0)  # 第一行默认为表头，数据第一行必须有表头
        self.save_dir = os.path.dirname(old_dir)

    def to_medical_his(self,exclusion=None):
        data = self.data.copy()
        save_path = os.path.join(self.save_dir, 'medical_history.xlsx')

        if exclusion == None:
            columns = list(data.columns.values)

        else:
            columns = set(data.columns.values) - set(exclusion)

        for column in columns:
            if {0,1} == set(data.loc[:,column].tolist()):
                data.loc[data[column]==1,[column]] = column
            else:
                data.loc[:,column].astype('str')
                data.loc[:,column] += column

        data.to_excel(save_path)

