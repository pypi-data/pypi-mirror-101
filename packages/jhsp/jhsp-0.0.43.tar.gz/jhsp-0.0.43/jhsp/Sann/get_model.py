import tensorflow as tf

import sys
import os

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

from Sann.models import sann,ann,sanntuner
from Sann import getweights,weights22netweights




class GetSannModel():
    """
    返回SANN模型和网络结构一样的ANN模型
    """
    def __init__(self,x,y,how):

        gw = getweights.GetWeights(x, y)
        self.weights = gw.GetW()


        if how == 'mull':
            self.final_activation = 'sigmoid'
            self.loss = tf.keras.losses.BinaryCrossentropy()
            self.metrics = 'accuracy'
        if how == 'mulc':
            self.final_activation = 'softmax'
            self.loss = 'categorical_crossentropy'
            self.metrics = 'accuracy'

    # 标签还是分类 ，加一个参数
    def GetSann(self,hp):

        model = sanntuner.Model(self.weights, self.final_activation,hp)
        model.compile(loss=self.loss, optimizer='adam', metrics=[self.metrics])

        return model

    def GetCorAnn(self,x, y, hidden_layers):
        """
        获得与SANN网络结构一致的ANN
        :return:
        """
        gw = getweights.GetWeights(x, y)
        w22n = weights22netweights.W22NW()
        initial_weigh,error = w22n.Weights2HW(gw.GetW(), hidden_layers, False)

        model = ann.Model(initial_weigh, self.final_activation)
        model.compile(loss=self.loss, optimizer='adam', metrics=[self.metrics])

        return model






