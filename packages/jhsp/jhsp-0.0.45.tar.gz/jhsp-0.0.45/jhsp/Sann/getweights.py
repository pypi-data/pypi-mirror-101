import pandas as pd
import os
import sys

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)



class GetWeights():
    """
    令i∈X为某一特征，J∈L为某一具体证型，S代表全体样本,具体见SANN论文
    :param x,y 为特征与诊断
    :param columns: 列名
    :param hidden_layer:  隐藏层节点数  如 [100,200,50]
    :return: 权值矩阵
    """

    def __init__(self,x,y,columns=None,index=None):

        self.x = x
        self.y = y

        self.index = index
        self.columns = columns

        self.Dij = {}
        self.Fi = {}
        self.Cj = {}
        self.R = {}

        self.W = [] # 特征数*标签数的一个矩阵，被self. GetW 赋值，类型是 dataframe
        self.WStandard = None

    def __GetD(self,i,j):
        """
        D值代表某一特征对某一证型的原始支持度，取值范围为[-0.5 ,0.5]。
        D值的绝对值越大，代表特征对证型的支持度越大，诊断意义也就越大。
        若D值的取值为正，则代表特征对证型有正向诊断意义；若取值为负，则代表特征对证型有负向诊断意义；
        若取值为0，则代表在诊断证型的时候无需考虑这一特征。
        :param i:   该特征在X矩阵中的列下标
        :param j:   该标签在Y矩阵中的列下标
        :return:  Dij = (Sij - (Sj/2)) / Sj
        """
        Sj = list(self.y.iloc[:,j] >= 1).count(True)

        Sij = list(self.x[self.y.iloc[:,j] >= 1].iloc[:,i] >= 1).count(True)

        Dij = (Sij - (Sj / 2)) / Sj

        return Dij

    def __GetF(self,i):
        """
        F值代表某一特征对所有证型的原始平均支持度，因此将特征对不同证型的支持度纳入了考虑。
        F值得计算与D值类似，但针对的是不同证型的所有患者。
        :param i:
        :return: Fi = (Si - (S / 2)) / S
        """

        S = self.x.shape[0]

        Si = list(self.x.iloc[:,i] >= 1).count(True)

        Fi = (Si - (S / 2)) / S

        return Fi

    def __GetC(self,j):
        """
        C的计算，依赖之前D的值
        C值反映了所有特征对某一证型的平均贡献度（与F值不同，F值代表某一特征对所有证型的平均贡献度），
        取值范围为[-0.5 ,0.5]。如果C值过高，则在进行证型预测时，很容易将其他证型的患者误判为这一证型；
        如果C值过低，则这一证型的患者不易被诊断。
        :param j:
        :return: Cj
        """
        Cj = 0

        for i in range(self.x.shape[1]):
            Cj += self.Dij[str(i) + str(j)]

        return Cj

    def __GetR(self):
        """
        R值代表的是所有特征对所有证型的平均贡献度，取值范围为[-0.5,0.5]。
        :return:
        """
        R = 0
        for i in range(self.x.shape[1]):
            R += self.Fi[str(i)]

        return R

    def __GetWij(self,i,j):
        """

        Wij = ((Dij - Fi) * (1 + abs(R-0.5)))/ (1 + (Cj - R))
        :param i:
        :param j:
        :return:
        """
        Dij = self.Dij[str(i) + str(j)]
        Fi = self.Fi[str(i)]
        Cj = self.Cj[str(j)]
        R = self.R

        Wij = ((Dij - Fi) * (1 + abs(R-0.5)))/ (1 + (Cj - R))

        return Wij

    def __GetWi(self,i):
        """
        获取某一特征对所有标签的权值
        :param i:
        :return: x2Y
        """
        Wi = []
        for j in range(self.y.shape[1]):
            Wi.append(self.__GetWij(i,j))

        return Wi

    def GetW(self):

        # 计算D、F并保存,key是str类型的数字
        for i in range(self.x.shape[1]):

            self.Fi[str(i)] = self.__GetF(i)

            for j in range(self.y.shape[1]):

                self.Dij[str(i) + str(j)] = self.__GetD(i,j)

        # 计算C/R 之所以分开是因为C、R的计算依赖D、F
        for j in range(self.y.shape[1]):
            self.Cj[str(j)] = self.__GetC(j)
        self.R = self.__GetR()



        for i in range(self.x.shape[1]):
            self.W.append(self.__GetWi(i))


        self.W = pd.DataFrame(data=self.W,index=self.index,columns=self.columns)

        return self.W

    def save(self,path='.\Weights.xlsx'):
        self.W.to_excel(path)





