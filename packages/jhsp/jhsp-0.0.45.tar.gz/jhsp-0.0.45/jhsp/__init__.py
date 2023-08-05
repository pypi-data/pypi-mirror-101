import os
import sys

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

# class Sann:
#
#
#     def __init__(self):
#         from Sann import getweights,get_model,weights22netweights
#         self.GetWeights = getweights.GetWeights
#         self.GetSannModel = get_model.GetSannModel
#         self.W22NW = weights22netweights.W22NW
#
# class Model:
#
#     def __init__(self):
#         from Model.trad_models_parameters import GetTraMandP
#
#         class Compare:
#             def __init__(self):
#                 from Model.Compare import get_model_score
#                 self.GetModelScores = get_model_score.GetModelScores
#
#         class Optimize:
#             def __init__(self):
#                 from Model.Optimize import get_best_model
#                 self.GetBestModel = get_best_model.GetBestModel
#
#         self.Compare = Compare
#         self.GetTraMandP = GetTraMandP
#         self.Optimize = Optimize
#
# class FunTools:
#     def __init__(self):
#         from FunTools import add_top_path,my_pow,my_split
#         self.add_top_path = add_top_path
#         self.my_pow = my_pow
#         self.my_split = my_split
#
# class ClassTools:
#     def __init__(self):
#         from ClassTools import collatingwords
#         self.CollatingWords = collatingwords.CollatingWords
#
# class Data:
#     def __init__(self):
#
#         class GetXY:
#             def __init__(self):
#                 from Data.GetXY import get_xy
#                 self.GetXY = get_xy.GetXY
#
#         class Preprocessing:
#             def __init__(self):
#                 from Data.Preprocessing import codingdata,describingdata,selectingfeatures
#                 self.CodingData = codingdata.CodingData
#                 self.DescribingData =describingdata.DescribingData
#                 self.SelectingFeatures = selectingfeatures.SelectingFeatures
#
#         class Standardization:
#             def __init__(self):
#                 from Data.Standardization import standardization
#                 self.Standardization = standardization
#
#
#         self.GetXY = GetXY
#         self.Preprocessing = Preprocessing
#         self.Standardization = Standardization

# Sann = Sann()
# Model = Model()
# FunTools = FunTools()
# ClassTools = ClassTools()
# Data = Data()















