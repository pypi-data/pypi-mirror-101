from sklearn.decomposition import NMF
import pandas as pd
import numpy as np
import pickle
from functools import reduce
import os
import sys

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)


class W22NW():

    def __init__(self):

        self.W = None
        self.DealW = None
        self.DealAgr = None
        self.hidden_layers = None
        self.HiddenWeights = None

    @staticmethod
    def __StandardScaler(W,how='go',arg_dict=None):


        if how == 'go':
            # 全局归一化
            mean = W.mean(axis=0).mean()
            std = W.std(axis=0).std()

            new_W = (W - mean) / std

            return new_W,{'mean':mean,'std':std}
        elif how == 'back':
            new_W = W * arg_dict['std'] + arg_dict['mean']
            return new_W

    @staticmethod
    def __ApplyOffset(W,how='go',arg_dict=None):

        if how == 'go':
            non_negative_offset = abs(W.min(axis=0).min())
            W += non_negative_offset
            return W,{'non_negative_offset':non_negative_offset}
        elif how == 'back':
            W -= arg_dict['non_negative_offset']
            return W

    @staticmethod
    def __MatrixFactorization(ori_W,inter_length):
        model = NMF(n_components=inter_length, init='random', random_state=0,max_iter=10000)
        W = model.fit_transform(ori_W)
        H = model.components_
        return W,H

    @staticmethod
    def GetError(W1,W2):

        error = W1 - W2
        error = abs(error).mean(axis=0).mean()
        return error

    def __PipDealWeights(self,W,how='go',DealAgr=None):

        if how == 'go':
            DealAgr_dict = {}

            new_W,SAgr = self.__StandardScaler(W)
            new_W,AAgr = self.__ApplyOffset(new_W)

            DealAgr_dict.update(SAgr)
            DealAgr_dict.update(AAgr)

            return new_W,DealAgr_dict

        if how == 'back':
            new_W = self.__ApplyOffset(W,how,DealAgr)
            new_W = self.__StandardScaler(new_W,how,DealAgr)
            return new_W

    def __GetOriWeights(self,HW,DealAgr):

        W = reduce(lambda x, y: np.matmul(x, y), HW)
        W = self.__PipDealWeights(W,how='back',DealAgr=DealAgr)
        return W

    def HiddenWeights2W(self,hd_path,save=True):

        with open(hd_path,'rb') as f:
            HD = pickle.load(f)

        HW = HD['HiddenWeights']
        DealAgr = HD['DealAgr']

        W = self.__GetOriWeights(HW,DealAgr)

        if save:
            pd.DataFrame(W,dtype=float).to_excel('.\HiddenWeights2W.xlsx')

        return W

    def Weights2HW(self,ori_W,hidden_layers,save=True):

        self.hidden_layers = hidden_layers
        self.ori_W = ori_W
        self.DealW,self.DealAgr = self.__PipDealWeights(ori_W)

        hidden_weights = []
        ori_w = self.DealW.copy()

        for hidden_nodes in self.hidden_layers:
            W,H = self.__MatrixFactorization(ori_w,hidden_nodes)
            hidden_weights.append(W)
            ori_w = H

        hidden_weights.append(H)

        self.HiddenWeights = hidden_weights

        HiddenWeights_DealAgr = {'HiddenWeights': self.HiddenWeights,
         'DealAgr': self.DealAgr
         }
        error = self.GetError(self.ori_W,self.__GetOriWeights(self.HiddenWeights,self.DealAgr))

        if save:
            with open('.\HiddenWeights_DealAgr.pk', 'wb') as f:
                pickle.dump({'HiddenWeights': self.HiddenWeights,
                             'DealAgr': self.DealAgr
                             }, f)

        return hidden_weights,error







