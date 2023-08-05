import os
import sys
import importlib
import shutil

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)


from sklearn.model_selection import RandomizedSearchCV
from kerastuner.tuners import RandomSearch

class GetBestModel():

    def __init__(self):


        if os.path.exists('config.py'):
            pass
        else:
            abs_path = os.path.abspath(__file__)
            dir = os.path.dirname(abs_path)
            default_config_path = os.path.join(dir,'default_config.py')
            shutil.copyfile(default_config_path,'config.py')

        import config

        self.config = config


    def GetBestTradition(self,model,parameters,x,y):
        """
        :param model_name:
        :param x:
        :param y:
        :return:
        """

        random_search = RandomizedSearchCV(model,
                                           param_distributions=parameters,
                                           n_iter=self.config.random_search_n_iter,
                                           cv=self.config.cross_val_num,
                                           scoring=self.config.scoring,
                                           random_state=self.config.random_num,
                                           n_jobs= self.config.random_search_n_jobs
                                           )

        random_search.fit(x, y)

        best_params = random_search.cv_results_['params'][random_search.best_index_]
        best_model = random_search.best_estimator_

        return best_model,best_params


    def GetBestNNet(self,model_fun,x,y,**kwargs):
        """
        超参数列表已经在构建模型的时候内置到模型里面了，所以不用传入，这人是用keras-tuner调参的一个特性，
        也是与传统调参方法不同的地方。
        """

        tuner = RandomSearch(
            model_fun,
            objective=self.config.scoring,  # 优化目标
            max_trials=self.config.max_trials,
            executions_per_trial=self.config.executions_per_trial,
            directory= model_fun.__name__ +'_dir',
            project_name= model_fun.__name__ ,
        )

        print(tuner.search_space_summary())

        tuner.search(x, y,
                     epochs=self.config.epochs_num,
                     )

        print(tuner.search_space_summary())
        print(tuner.results_summary())


        return tuner.get_best_models(num_models=1), tuner.results_summary(num_trials=1)













