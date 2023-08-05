import os
import sys
import numpy as np
import pickle

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

class GetXY():
    """

    """
    def __init__(self):
        pass

    def GetCrossXY(self,x,y,k,save=False):

        save_path = 'CrossValXY.pkl'

        xy_cross_val_list = []

        random_list = [i for i in range(x.shape[0])]
        np.random.shuffle(random_list)

        cross_num = x.shape[0] // k


        for time in range(k):
            if time == k-1:
                xy_cross_val_list.append((x.iloc[random_list, :],
                                          y.iloc[random_list[0:cross_num],:])
                                         )
                break

            xy_cross_val_list.append((x.iloc[random_list[0:cross_num],:],
                                      y.iloc[random_list[0:cross_num],:])
                                     )
            del random_list[0:cross_num]

        if save:
            with open(save_path,'wb') as f:
                pickle.dump(xy_cross_val_list,f)

        return xy_cross_val_list

    @staticmethod
    def LoadCrossXY(path):
        with open(path,'wb') as f:
            xy_cross_val_list = pickle.load(f)
            return xy_cross_val_list










