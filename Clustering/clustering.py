from sklearn import mixture, cluster
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection

def vbgmm(vecs, vecs_input):
    gmm = mixture.BayesianGaussianMixture(n_components=1000).fit(vecs)
    results = gmm.predict(vecs_input)
    print(results)

def meanshift(vecs, vecs_input):
    ms = cluster.MeanShift().fit(vecs)
    results = ms.predict(vecs_input)
    print(results)

# def vbgmm_tuning(df):
#     tuned_parameters = [
#         {'n_components': [10, 100, 1000], 'covariance_type': ['spherical', 'tied', 'diag', 'full'], 'max_iter': [10, 100, 1000], 'n_init': [1, 10, 100], 'init_params': ['kmeans', 'random'], 'weight_concentration_prior_type': ['dirichlet_process', 'dirichlet_distribution'], 'weight_concentration_prior': [None, 0.5, 1, 10, 100], 'mean_precision_prior': [None, 0.5, 1, 10, 100], 'degrees_of_freedom_prior': [None, 1, 10, 100, 1000], 'warm_start': [True, False]}
#     ]
#     svc_grid = GridSearchCV(estimator=mixture.BayesianGaussianMixture(),
#                     param_grid = tuned_parameters,
#                     scoring="accuracy",
#                     cv = 3,
#                     n_jobs=1)
#     svc_grid.fit(data_train, label_train)
#     return svc_grid.best_params_