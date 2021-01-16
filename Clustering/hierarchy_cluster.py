def hierarchy_cluster(df):
    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
    linkage_result = linkage(df, method='ward', metric='euclidean')
    return linkage_result