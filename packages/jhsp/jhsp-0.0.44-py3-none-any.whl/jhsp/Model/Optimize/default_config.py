# 公共模型参数配置
scoring = 'accuracy'
cross_val_num = 5
metrics_list = ['accuracy', 'precision', 'recall', 'f1']
random_num = 100



# sklearn-RandomizedSearchCV 超参数调优参数配置
random_search_n_iter = 100
random_search_n_jobs = -1


# keras-tuner 超参数调优参数配置
epochs_num = 1000
max_trials = 50
executions_per_trial = 2