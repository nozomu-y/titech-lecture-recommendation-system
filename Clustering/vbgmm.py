from sklearn import mixture
import pandas as pd

def vbgmm(df, df_input):
    gmm = mixture.GaussianMixture(n_components=1000).fit(df)
    results = gmm.fit_predict(df_input)
    print(results)