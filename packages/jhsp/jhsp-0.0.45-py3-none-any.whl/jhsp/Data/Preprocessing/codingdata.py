import pandas as pd
import os
import warnings
import sys
import tqdm

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

# 因为在进行编码的时候，会对一些汉字描述的特征进行编码，如：轻度编码为1，重度编码为2。
# 在进行DataFrame的筛选时，就会出现比较 汉字str与编码int的情况，因此会出现警告信息。
# 这个警告信息可以忽略。
warnings.filterwarnings(action='ignore',message='elementwise comparison failed')

class CodingData():
    """
    这是一个编码数据的类，包括将one数据转换为onehot数据，将onehot数据转化为one数据，编码分类信息，编码等级信息等。
    本类中所有函数的参数都以列表形式传入。
    """
    def __init__(self):
        pass

    def onehot2one(self,columns):
        """
        本函数功能是将onehot编码的多列转化为one编码的一列。
        :param columns: 是一个列表，列表元素是需要转化的列名 如 ['column1','column2']
        直接将修改self.data
        """

        y_onehot = self.data.loc[:,columns].copy()   # 将要转化的列取出来
        new_column_name = "+".join(columns)

        # 增添一个列，列名=要转化的列的列名拼接起来，值为0
        y_onehot.loc[:, new_column_name] = pd.Series([0 for i in range(y_onehot.shape[0])])

        # 遍历要转化的每一个列，按照其在列表中的顺序，对其为1的值进行编码。第一列为1的转化为1，第二列为1的转化为2，以此类推
        # 因为onehot编码的数据，一行只有一个1。因此在进行上一行所述的编码操作之后，令新的列的值等onehot列的和
        # 这个和的值就可以代表该行的onehot分类
        for i,y_column in enumerate(columns,start=1):
            y_onehot.loc[y_onehot[y_column]==1,[y_column]] = i   #依次对每一列中为1的值进行编码，数字每次加1
            y_onehot.loc[:, new_column_name] += y_onehot[y_column].values  # one列的值等于之前所有列的和。


        for i, y_column in enumerate(columns,start=1):

            # 将one列的值，从数字编码转化为原onehot编码的列名
            y_onehot.loc[y_onehot[new_column_name]==i,[new_column_name]] = y_column


        self.data.drop(columns,axis=1,inplace=True)         # 删除原onehot列
        self.data.loc[:,new_column_name] = y_onehot.loc[:,new_column_name].copy() # 将新列赋值给self.data

    def one2onehot(self,one_columns):
        """
        这个函数将一列，转化为onehot编码的多列
        :param one_columns:
        :return:
        """

        # 从要转化为onehot的多个列中一次选出一个进行转化
        for one_column in one_columns:

            # 将这个列的值作为转化后onehot列的列名
            columns = set(self.data.loc[:,one_column].values.flatten())

            for column in columns:   # 遍历每一个将要新建的onehot列名
                new_column = one_column + column # 为了便于区分，onehot列名之前要加上原列的列名
                # 用定义的列名，新建一个onehot列，其值为0
                self.data.loc[:,new_column] = pd.Series([0 for i in range(self.data.shape[0])])
                # 筛选出原列中，值为新建列列名的行，在新建列中将该行赋值为1
                self.data.loc[self.data[one_column]==column,[new_column]] = 1

        self.data.drop(one_columns, axis=1, inplace=True)

    def grades22(self,regulations):
        """
        本函数是将分级数据转化为二分类数据，参数是转化规则，本质是一个列表，列表元素是元组如：【（‘轻度’，0），（“重度”，1）】

        """
        # 遍历所有列
        for column in self.data.columns.values:
            for item in regulations:
                # 对每一列，遍历规则，改为2分类数据
                self.data.loc[self.data[column] == item[0],[column]] = item[1]

    def coding_y(self,y_column):
        """
        本函数功能是将y进行编码，并将编码关系储存到数据目录下。参数为一个列表：【‘列名’】
        :param y_column:
        :return:
        """
        y_names = set(self.data.loc[:, y_column].values.flatten())

        coded_relationship = []
        for i,y_name in enumerate(y_names):
            self.data.loc[self.data[y_column[0]]==y_name,[y_column[0]]] = i
            coded_relationship.append((i, y_name))

        save_dir = os.path.join(self.save_dir,'coded_relationship.txt')
        with open(save_dir,'w',encoding='utf-8') as f:
            for item in coded_relationship:
                f.write(str(item[0]) + ': ' + item[1] + '\n')

    @staticmethod
    def content2features(data,content_column_name):

        # 获取所有的特征列表
        features_list = []
        for row in range(data.shape[0]):
            features_list.extend(data.loc[row,content_column_name].split(','))

        features_list = list(set(features_list))
        features_list.remove('')



        # 生cheng特征列，默认值为0
        for feature in features_list:
            data[str(feature)] = 0

        #
        for row in tqdm.tqdm(range(data.shape[0])):
            row_features_list =  data.loc[row, content_column_name].split(',')
            for row_feature in row_features_list:
                data.loc[row,row_feature] = 1

        del data[content_column_name]


        return data,features_list

    def save(self):
        self.data.to_excel(self.save_path,index=False)

