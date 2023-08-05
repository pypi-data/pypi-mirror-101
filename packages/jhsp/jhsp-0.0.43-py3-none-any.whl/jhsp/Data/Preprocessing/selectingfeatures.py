import pandas as pd
import os
import numpy as np
import sys

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)

class SelectingFeatures():

    def __init__(self, old_dir, standardization=None, balance=False):
        self.data = self.data = pd.read_excel(old_dir,header=0)   # 第一行默认为表头，数据第一行必须有表头
        self.save_dir = os.path.dirname(old_dir)       # 默认保存路径为原数据同一目录
        self.x = self.data.iloc[:,:-1]
        self.y = self.data.iloc[:, -1]

        if balance:
            self.__balancing_sample()

        if standardization == 'MM':
            from sklearn.preprocessing import MinMaxScaler
            self.x = MinMaxScaler().fit_transform(self.x)
        elif standardization == 'SS':
            from sklearn.preprocessing import StandardScaler
            self.x = StandardScaler().fit_transform(self.x)

    def __balancing_sample(self):
        from imblearn.over_sampling import SMOTE
        sm = SMOTE(random_state=100)
        self.x, self.y = sm.fit_sample(self.x, self.y)

    def save_weight(self,name,weight,index=None):
        save_path = os.path.join(self.save_dir, 'weight')
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        save_path = os.path.join(save_path, '{}.xlsx'.format(name))

        if index == None:
            index = self.data.iloc[:,:-1].columns.values


        weight = np.array(weight).reshape(-1,1)
        weight_df =  pd.DataFrame(data=weight, index=index, columns=['weight'])
        weight_df.sort_values('weight', inplace=True,ascending=False)

        weight_df.to_excel(save_path)
        return weight_df

    def filter_variance(self):
        from sklearn.feature_selection import VarianceThreshold
        vt = VarianceThreshold().fit(self.x,self.y)
        variances = vt.variances_
        return self.save_weight('variances', variances)

    def filter_correlation(self,how='pearsonr'):

        if how == 'pearsonr':
            correlation = self.data.corr(method='spearman').iloc[:-1,-1]

        return self.save_weight('cor_{}'.format(how), correlation)

    def filter_mutual_info(self,how='mRMR'):

        def get_entropy(variables):
            from collections import Counter

            var_times_dict = Counter(variables)
            var_list = set(variables)
            all_times = len(variables)
            entropy = 0

            for x in var_list:
                p = var_times_dict[x] / all_times
                log = np.log2(p)
                entropy -= p * log

            return entropy

        def get_conditional_entropy(variables,cond_vars):
            from collections import Counter

            cond_var_times_dict = Counter(cond_vars)
            cond_var_set = set(cond_vars)
            entropy = 0

            for cond_var in cond_var_set:

                p1 = cond_var_times_dict[cond_var] / len(cond_vars)

                var_by_cvar = []
                for i,cond_var2 in enumerate(cond_vars):
                    if cond_var == cond_var2:
                        var_by_cvar.append(variables[i])

                var_times_dict = Counter(var_by_cvar)
                var_set = set(var_by_cvar)

                temp = 0
                for var in var_set:
                    p2 = var_times_dict[var] / len(var_by_cvar)
                    log2 = np.log2(p2)
                    temp += p2 * log2

                entropy -= p1 * temp

            return entropy

        def get_mul_info(variables,cond_vars):
            return get_entropy(variables) - get_conditional_entropy(variables,cond_vars)

        def mRMR(M,S,c):

            sequences = []

            if S.shape[1] == 0:
                m_name_list = list(M.columns.values)
                for m_name in m_name_list:
                    m = M.loc[:, m_name]
                    score = get_mul_info(m, c)
                    sequences.append((m_name, score))

                return sequences



            m_name_list = list(M.columns.values)
            s_name_list = list(S.columns.values)

            for m_name in m_name_list:

                m = M.loc[:,m_name]


                s_sum = 0
                for s_name in s_name_list:
                    s = S.loc[:, s_name]
                    s_sum += get_mul_info(m,s)

                s_sum *= 1/len(S)

                score = get_mul_info(m,c) - s_sum

                sequences.append((m_name,score))

            return sequences

        def get_features(how=how):

            if how == 'mRMR':
                get_score = mRMR

            c = self.y
            M = pd.DataFrame(data=self.x,columns=self.data.iloc[:,:-1].columns.values)
            S = pd.DataFrame()

            all_x = self.x.shape[1]

            outcome = []

            while S.shape[1] < all_x:
                M_score = get_score(M, S, c)
                sorted(M_score,key=lambda x:x[1],reverse=True)

                selected_m = M_score[0][0]
                S = pd.concat([S,M.loc[:,selected_m]],axis=1)
                del M[selected_m]

                outcome.append(M_score[0])

            weight = [i[1] for i in outcome]
            index = [i[0] for i in outcome]
            self.save_weight('mulinfo_mRMR', weight, index)

        get_features(how)

    def wrapper_sfs(self,estimator_name='SVC',direction='forward'):
        import numbers
        import numpy as np
        from sklearn.feature_selection._base import SelectorMixin
        from sklearn.base import BaseEstimator, MetaEstimatorMixin, clone
        from sklearn.utils._tags import _safe_tags
        from sklearn.utils.validation import check_is_fitted
        from sklearn.model_selection import cross_val_score

        class SequentialFeatureSelector(SelectorMixin, MetaEstimatorMixin,
                                        BaseEstimator):
            """Transformer that performs Sequential Feature Selection.

            This Sequential Feature Selector adds (forward selection) or
            removes (backward selection) features to form a feature subset in a
            greedy fashion. At each stage, this estimator chooses the best feature to
            add or remove based on the cross-validation score of an estimator.

            Read more in the :ref:`User Guide <sequential_feature_selection>`.

            .. versionadded:: 0.24

            Parameters
            ----------
            estimator : estimator instance
                An unfitted estimator.

            n_features_to_select : int or float, default=None
                The number of features to select. If `None`, half of the features are
                selected. If integer, the parameter is the absolute number of features
                to select. If float between 0 and 1, it is the fraction of features to
                select.

            direction: {'forward', 'backward'}, default='forward'
                Whether to perform forward selection or backward selection.

            scoring : str, callable, list/tuple or dict, default=None
                A single str (see :ref:`scoring_parameter`) or a callable
                (see :ref:`scoring`) to evaluate the predictions on the test set.

                NOTE that when using custom scorers, each scorer should return a single
                value. Metric functions returning a list/array of values can be wrapped
                into multiple scorers that return one value each.

                If None, the estimator's score method is used.

            cv : int, cross-validation generator or an iterable, default=None
                Determines the cross-validation splitting strategy.
                Possible inputs for cv are:

                - None, to use the default 5-fold cross validation,
                - integer, to specify the number of folds in a `(Stratified)KFold`,
                - :term:`CV splitter`,
                - An iterable yielding (train, test) splits as arrays of indices.

                For integer/None inputs, if the estimator is a classifier and ``y`` is
                either binary or multiclass, :class:`StratifiedKFold` is used. In all
                other cases, :class:`KFold` is used.

                Refer :ref:`User Guide <cross_validation>` for the various
                cross-validation strategies that can be used here.

            n_jobs : int, default=None
                Number of jobs to run in parallel. When evaluating a new feature to
                add or remove, the cross-validation procedure is parallel over the
                folds.
                ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
                ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
                for more details.

            Attributes
            ----------
            n_features_to_select_ : int
                The number of features that were selected.

            support_ : ndarray of shape (n_features,), dtype=bool
                The mask of selected features.

            See Also
            --------
            RFE : Recursive feature elimination based on importance weights.
            RFECV : Recursive feature elimination based on importance weights, with
                automatic selection of the number of features.
            SelectFromModel : Feature selection based on thresholds of importance
                weights.

            Examples
            --------
            >>> from sklearn.feature_selection import SequentialFeatureSelector
            >>> from sklearn.neighbors import KNeighborsClassifier
            >>> from sklearn.datasets import load_iris
            >>> X, y = load_iris(return_X_y=True)
            >>> knn = KNeighborsClassifier(n_neighbors=3)
            >>> sfs = SequentialFeatureSelector(knn, n_features_to_select=3)
            >>> sfs.fit(X, y)
            SequentialFeatureSelector(estimator=KNeighborsClassifier(n_neighbors=3),
                                      n_features_to_select=3)
            >>> sfs.get_support()
            array([ True, False,  True,  True])
            >>> sfs.transform(X).shape
            (150, 3)
            """

            def __init__(self, estimator, *, n_features_to_select=None,
                         direction='forward', scoring=None, cv=5, n_jobs=None):

                self.estimator = estimator
                self.n_features_to_select = n_features_to_select
                self.direction = direction
                self.scoring = scoring
                self.cv = cv
                self.n_jobs = n_jobs

            def fit(self, X, y):
                """Learn the features to select.

                Parameters
                ----------
                X : array-like of shape (n_samples, n_features)
                    Training vectors.
                y : array-like of shape (n_samples,)
                    Target values.

                Returns
                -------
                self : object
                """
                tags = self._get_tags()
                X, y = self._validate_data(
                    X, y, accept_sparse="csc",
                    ensure_min_features=2,
                    force_all_finite=not tags.get("allow_nan", True),
                    multi_output=True
                )
                n_features = X.shape[1]

                error_msg = ("n_features_to_select must be either None, an "
                             "integer in [1, n_features - 1] "
                             "representing the absolute "
                             "number of features, or a float in (0, 1] "
                             "representing a percentage of features to "
                             f"select. Got {self.n_features_to_select}")
                if self.n_features_to_select is None:
                    self.n_features_to_select_ = n_features // 2
                elif isinstance(self.n_features_to_select, numbers.Integral):
                    if not 0 < self.n_features_to_select < n_features:
                        raise ValueError(error_msg)
                    self.n_features_to_select_ = self.n_features_to_select
                elif isinstance(self.n_features_to_select, numbers.Real):
                    if not 0 < self.n_features_to_select <= 1:
                        raise ValueError(error_msg)
                    self.n_features_to_select_ = int(n_features *
                                                     self.n_features_to_select)
                else:
                    raise ValueError(error_msg)

                if self.direction not in ('forward', 'backward'):
                    raise ValueError(
                        "direction must be either 'forward' or 'backward'. "
                        f"Got {self.direction}."
                    )

                cloned_estimator = clone(self.estimator)

                # the current mask corresponds to the set of features:
                # - that we have already *selected* if we do forward selection
                # - that we have already *excluded* if we do backward selection
                current_mask = np.zeros(shape=n_features, dtype=bool)

                self.ranking = list(np.zeros(shape=n_features, dtype=int))

                n_iterations = (
                    self.n_features_to_select_ if self.direction == 'forward'
                    else n_features - self.n_features_to_select_
                )
                for _ in range(n_iterations):
                    new_feature_idx = self._get_best_new_feature(cloned_estimator, X,
                                                                 y, current_mask)
                    current_mask[new_feature_idx] = True

                    if self.direction != 'backward':
                        self.ranking[new_feature_idx] = n_features - _
                    else:
                        self.ranking[new_feature_idx] = -(n_features - _)

                if self.direction == 'backward':
                    current_mask = ~current_mask
                self.support_ = current_mask

                return self

            def _get_best_new_feature(self, estimator, X, y, current_mask):
                # Return the best new feature to add to the current_mask, i.e. return
                # the best new feature to add (resp. remove) when doing forward
                # selection (resp. backward selection)
                candidate_feature_indices = np.flatnonzero(~current_mask)
                scores = {}
                for feature_idx in candidate_feature_indices:
                    candidate_mask = current_mask.copy()
                    candidate_mask[feature_idx] = True
                    if self.direction == 'backward':
                        candidate_mask = ~candidate_mask
                    X_new = X[:, candidate_mask]
                    scores[feature_idx] = cross_val_score(
                        estimator, X_new, y, cv=self.cv, scoring=self.scoring,
                        n_jobs=self.n_jobs).mean()
                return max(scores, key=lambda feature_idx: scores[feature_idx])

            def _get_support_mask(self):
                check_is_fitted(self)
                return self.support_

            def _more_tags(self):
                return {
                    'allow_nan': _safe_tags(self.estimator, key="allow_nan"),
                    'requires_y': True,
                }

        if estimator_name == 'SVC':
            from sklearn.svm import SVC
            estimator = SVC()

        if estimator_name == 'KNN':
            from sklearn.neighbors import KNeighborsClassifier
            estimator = KNeighborsClassifier()

        sfs = SequentialFeatureSelector(estimator, direction=direction, n_features_to_select=2,).fit(self.x, self.y)


        weight = sfs.ranking

        return self.save_weight('wrapper_{}'.format(estimator_name),weight)

    def embedded_rfe(self,estimator_name='LSVC'):
        from sklearn.feature_selection import RFE

        if estimator_name == 'LSVC':
            from sklearn.svm import LinearSVC
            estimator = LinearSVC()
        elif estimator_name == 'LASSO':
            from sklearn.linear_model import LassoCV
            estimator = LassoCV()



        ref = RFE(estimator=estimator, n_features_to_select=1, step=1)
        ref.fit(self.x, self.y)
        weight = ref.ranking_

        n = self.x.shape[1]

        reverse_weight = []
        order_dict = dict(zip(range(1,n+1,1),range(n,0,-1)))
        for i in weight:
            reverse_weight.append(order_dict[i])

        self.save_weight('embedded_rfe_{}'.format(estimator_name), reverse_weight)

    def embedded_lasso(self):
        from sklearn.linear_model import LassoCV

        # x = StandardScaler().fit_transform(x)  # lasso必须先标准化

        lasso = LassoCV(cv=5) # 最优alpha竟然是0.00012463621602719477，所有千万不要自己设置字典，就用自动的才行
        lasso.fit(self.x, self.y)
        weight = lasso.coef_
        self.save_weight('wrapper_lasso', weight)

    def embedded_gbdt(self):
        from sklearn.ensemble import GradientBoostingClassifier
        from sklearn.model_selection import GridSearchCV


        param = {'learning_rate': [0.1,0.2,0.3],
                 'n_estimators': [i for i in range(100,500,100)],
                 'min_samples_split':[i for i in range(2,4,1)],
                 'max_depth':[i for i in range(3,4,1)]}
        grid_search = GridSearchCV(GradientBoostingClassifier(),param , scoring='accuracy', cv=None)
        grid_search.fit(self.x, self.y)


        model = grid_search.best_estimator_.fit(self.x, self.y)
        weight = model.feature_importances_
        self.save_weight('embedded_gbdt', weight)

    def embedded_rf(self):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import GridSearchCV

        param = {'n_estimators': [i for i in range(100,500,100)],
                 'min_samples_split':[i for i in range(2,4,1)],
                 'max_depth':[i for i in range(3,4,1)]}

        grid_search = GridSearchCV(RandomForestClassifier(),param , scoring='accuracy', cv=None)
        grid_search.fit(self.x, self.y)


        model = grid_search.best_estimator_.fit(self.x, self.y)
        weight = model.feature_importances_
        self.save_weight('embedded_rf', weight)

    def embedded_sann(self):
        pass

