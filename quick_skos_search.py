#!/usr/bin/env python

#searches ./data/index/skosNodeNames.dict to check if a particular word is present in skos subgraph

import pickle
import utils as ut
import collections
import math
import numpy as np

def searchIndex(target):
    # target='word1 word2'
    f=open('./data/index/skosNodeNames.dict','r')
    searchterms = [] # target list
    for t1 in target.split(' '):
        searchterms.append(t1.lower())
    skosAll=pickle.load(f)
    seen=0
    flag=0
    maxMatch=0
    matchD={}
    for sg in skosAll.keys():
        subg = sg
        # iterate over all nodes in subgraph
        for node in skosAll[subg]:
            seen+=1
            node_words=[]
            for n in node.split('_'):
                node_words.append(n.lower())
            r=len(set(searchterms).intersection(set(node_words)))
            if r>0:
                matchD[node]=r
                flag=1
    if flag==0:
        print 'Not found'
    sim = node_based_sim(matchD)
    #if matchD<1==Node:
    #    confi=.00001
    #elif len(matchD)>0:
    #    confi = math.log(len(matchD))
    #else:
    #    confi=0.0000001
    #sim2 = (sim*confi)/100
    if sim!=0:
        sim2=sim
    else:
        sim2=len(matchD)*1.0/seen
    return sim2, len(matchD)
    
def node_based_sim(matchD):
    vals = matchD.values()
    counter=collections.Counter(vals)
    del counter[1]
    freqD=ut.dtsort(counter,1,'desc')
    print freqD
    print ''
    fvals=ut.tupCollect(freqD[:100],1)
    sim = 0
    index=0
    for f in fvals:
        index+=1
        sim+=(f*1.0)/math.pow(2,index)
    return sim
        
    
if __name__ == '__main__':
    target = raw_input('Enter target words: ')
    sim, hits= searchIndex(target)
    print 'Total hits: ', hits
    print 'similarity: ', sim
