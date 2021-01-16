def GetScoreClus(keys,gmm):
    import getname
    score=0
    for doc, cls in zip(keys, gmm):
        num=gmm.tolist().count(cls)
        lis=getname.GetRelaSub(doc)
        lis2=[]
        for doc2, cls2 in zip(keys, gmm):
            if cls2==cls:
                lis2.append(doc2)
        score+=len(set(lis2)&set(lis))+1/num
    score/=len(gmm)
    return score
    
    
