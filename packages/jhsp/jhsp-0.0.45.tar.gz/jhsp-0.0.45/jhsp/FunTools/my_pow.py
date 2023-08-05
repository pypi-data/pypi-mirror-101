from math import pow
from pandas import Series

def my_pow(x,y):
    """
    增加对 series等的支持
    :return:
    """
    try:
        list(x)
    except TypeError:    # 如果是一个数，就会类型错误，如果本身就是series或者list 就不会报错
        return pow(x,y)
    else:
        new_x = x.copy()

        for i in range(len(x)):
            new_x[i] = pow(x[i],y)

        # 返回与X数据类型一致的结果

        if isinstance(x,list):
            return new_x

        elif isinstance(x,Series):
            return Series(new_x)