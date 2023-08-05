
from sklearn import metrics
from sklearn.model_selection import KFold

import os
import sys

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)






class GetModelScores():
    """

    """

    def __init__(self):
        pass

    def GetScoresCross(self,model,x,y,k):
        """

        :param model:
        :param x:
        :param y:
        :return:
        """

        kfold = KFold(n_splits=k, shuffle=True)

        score_dict = {}
        acc_score_list = []
        pre_score_list = []
        rec_score_list = []
        f1_score_list = []


        for train_index,test_index in kfold.split(x,y):


            train_x = x.iloc[train_index,:]
            train_y = y.iloc[train_index,:]
            test_x = x.iloc[test_index,:]
            test_y = y.iloc[test_index,:]


            model.fit(train_x, train_y)
            pre_y = model.predict(test_x)


            acc_score_list.append(metrics.accuracy_score(test_y,pre_y))

            pre_score_list.append(metrics.precision_score(test_y,pre_y, average='macro'))

            rec_score_list.append(metrics.recall_score(test_y,pre_y, average='macro'))

            f1_score_list.append(metrics.f1_score(test_y,pre_y, average='macro'))




        score_dict['accuracy'] = acc_score_list
        score_dict['precision'] = pre_score_list
        score_dict['recall'] = rec_score_list
        score_dict['f1'] = f1_score_list

        return score_dict

