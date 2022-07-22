# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 10:13:00 2020

@author: abazin
"""

import subprocess
import os
from subprocess import PIPE
import copy
import numpy as np


pca_shd_exec_path = "/home/alexandre/Documents/Recherche/Code/PolyConcAnalysis/PCA/shd"

def set_shd_path(p):
    pca_shd_exec_path = p


'''
Set manipulation functions
'''

#tests whether the last n-1 components of concept A are included in the last n-1 components of concept B
def subsetConcepts(A,B):
    sub = True
    for i in range(1,len(A)):
        if not A[i].issubset(B[i]):
            sub = False
    return sub



#Cartesian product of a family F of sets and [0,n-1]
def combi(F,n):
    R = []

    for f in F:
        for x in range(n):
            f2 = copy.deepcopy(f)
            f2.append(int(x))
            R.append(f2)
    
    return R



#Cartesian product of a family F of sets and a set S
def combiSet(F,S):
    R = []

    for f in F:
        for x in S:
            f2 = copy.deepcopy(f)
            f2.append(int(x))
            R.append(f2)
    
    return R



#Logical / transitive closure of a set by a set of implication rules
def logicalClosure(Set,Rules):
    S = copy.copy(Set)
    fin = False    
    while not fin:
        s = len(S)
        for I in Rules:
            if I[0].issubset(S):
                S = S.union(I[1])
        if len(S) == s:
            fin = True         
    return set(S)



'''
Transversals computation functions
'''


#Create a file containing the complement of the context
def makeHypergraphFile(context,file):
    f = open(file,"w")
    
    C = [[]]
    for i in range(len(context)-1):
        C = combi(C,context[i+1])
    
    for c in C:
        if c not in context[0]:
            summ=0
            for e in range(len(c)-1):
                f.write(str(summ+c[e]))
                f.write(",")
                summ=summ+context[e+1]
            f.write(str(summ+c[len(c)-1]))
            f.write("\n")
    
    f.close()
    
  
#Creates a concept from a transversal by complementing 
def trans2Concept(trans,context):
    
    Concept = []
    summ = 0
    for i in range(1,len(context)):
        Comp = []
        for e in range(summ, summ+context[i]):
            if str(e) not in trans:
                Comp.append(int(e-summ))
        Concept.append(set(Comp))
        summ += context[i]
    
    return Concept


def minTrans(hypergraph):
    args = [pca_shd_exec_path,"0",hypergraph,"-"]
    p = subprocess.Popen(args, stdin=PIPE, stdout=PIPE, text=True)
    M =  p.communicate()[0]
    
    R = []
    
    T = M.split("\n")   
    if len(T) > 1: 
        maxiC = 0
        for x in T:
            c = x.split(" ")
            R.append(c)
            if len(c) > maxiC:
                maxiC = len(c)
        for i in range(maxiC+3):
            R.pop(len(R)-1)
    else:
        print("shd did not return anything\n")
    return R
                

'''
FCA functions
'''

#Computes the intent of a set of objects in a context
def Intent(S,context):
    R = set([])
    for a in range(context[2]):
        add = True
        for o in S:
            if [o,a] not in context[0]:
                add = False
        if add:
            R.add(a)
    return R
            

    #COmputes the extent of a set of attributes in a context
def Extent(S,context):
    R = set([])
    for o in range(context[1]):
        add = True
        for a in S:
            if [o,a] not in context[0]:
                add = False
        if add:
            R.add(o)
    return R



def oplus(A, a, context):
    B = copy.deepcopy(A)
    for x in A:
        if x > a:
            B.remove(x)
    B.add(a)
    B = Extent(Intent(set(B), context), context)
    return B



def Next(A, context):
    for i in reversed(range(context[1])):
        if not i in A:
            B = oplus(A, i, context)
            fin = True
            for j in B:
                if j < i and j not in A:
                    fin = False
            if fin:
                return B


#Computes the concepts of a bidimensional context
def NextClosure(context):
    Concepts = []
    A = Extent(Intent(set([]),context),context)
    while len(A) < context[1]:
        Concepts.append([A, Intent(A, context)])
        A = Next(A, context)
    Concepts.append([A, Intent(A, context)])
    return Concepts



def oplusDG(A, a, imp):
    B = copy.deepcopy(A)
    for x in A:
        if x > a:
            B.remove(x)
    B.add(a)
    B = logicalClosure(B, imp)
    return B



def NextDG(A, imp, nbAtt):
    for i in reversed(range(nbAtt)):
        if not i in A:
            B = oplusDG(A, i, imp)
            fin = True
            for j in B:
                if j < i and j not in A:
                    fin = False
            if fin:
                return B



#Flattens a multidimensional context
def multi2Bi(context):
    
    elems = {}
    #size of the new dimension
    C = [[]]
    for i in range(len(context)-2):
        C = combi(C,context[i+2])
    for c in range(len(C)):
        elems[c] = C[c]
        
    ncontext = [[],context[1],len(C)]
    
    for t in context[0]:
        T = np.array(t)
        for i in range(len(C)):
            if elems[i] == list(T[1:]):
                ncontext[0].append([T[0],i])
                break

    
    return ncontext,elems


def aMinGenImp(Set,Implis):
    G = copy.deepcopy(Set)
    Ferm = logicalClosure(Set,Implis)
    for s in Set:
        G.remove(s)
        if logicalClosure(G,Implis) != Ferm:
            G.add(s)
    return G



def allMinGensImp(Set,Implis):
    MG = [aMinGenImp(Set,Implis)]
    for G in MG:
        for I in Implis:
            X = copy.deepcopy(G)
            X = X.union(I[0])
            X = X.union(I[1])
            if X.issubset(Set):
                Y = copy.deepcopy(I[0])
                Z = copy.deepcopy(G)
                Z = Z.difference(I[1])
                Y = Y.union(Z)
                flag = True
                for H in MG:
                    if H.issubset(Y):
                        flag = False
                if flag:
                    NG = aMinGenImp(Y,Implis)
                    MG.append(NG)
    return MG


#Returns slices of a context that correspond to an element of a dimension
def sliceContext(context,element,dimension):
    R = []
    for X in context[0]:
        if X[dimension] == element:
            Y = copy.deepcopy(X)
            Y.pop(dimension)
            R.append(Y)
    C = list(copy.deepcopy(context))
    C[0] = R
    C.pop(dimension+1)
    return tuple(C)



#Returns the support on a dimension of a n-1 concept
def support(concept,context,dimension):
    R=set([])
    
    prod = [[]]
    for C in concept:
        prod = combiSet(prod,C)
        
    for e in range(context[dimension+1]):
    
        oui = True
        for X in prod:
            Y = copy.deepcopy(X)
            Y.insert(dimension,e)
            if Y not in context[0]:
                oui = False
                break
        
        if oui:
          R.add(e)
          
    return R



'''
Main functions
'''


#Compute the concepts of a context
def concepts(context):
    Concepts = []
    
    #Create file for shd.exe
    makeHypergraphFile(context,"hypergraph.io")
    
    #run shd.exe to obtain minimal tranversals
    Concepts = minTrans("hypergraph.io")
    
    #delete the file
    os.remove("hypergraph.io")
    

    
    #Complement the transversals to get the concepts
    for i in range(len(Concepts)):
        Concepts[i] = trans2Concept(Concepts[i],context)
    
    return Concepts



#Builds an implication base from the proper premises of a 2D context
def properPremises(context):
    
    table = []
    
    if len(context) > 3:
        context,table = multi2Bi(context)
    
    Attributes = set(np.array(context[0])[:,1])
    
    Base = []
    
    #for each attribute a
    for a in Attributes:
        
        #find the objects that do not have a
        Obj_a = set([])
        for t in context[0]:
            if t[1] == a:
                Obj_a.add(t[0])
        Obj_a = set(range(context[1])).difference(Obj_a)
                
        #construct a hypergraph by complementing the intents of these objects
        hypergraph = open("hypergraph_proper.io","w")
        for o in Obj_a:
            first = False
            for b in range(context[2]):
                if [o,b] not in context[0]:
                    if not first:
                        hypergraph.write(" ")
                    hypergraph.write(str(b))
            hypergraph.write("\n")
            
        hypergraph.close()
        
        #The premises are the minimal transversals of the hypergraph
        Prem = minTrans("hypergraph_proper.io")
        for p in Prem:
            q = []
            for e in p:
                q.append(int(e))
            if not (len(q) == 1 and q[0] == a):
                Base.append([set(q),set([a])])
        
        os.remove("hypergraph_proper.io")
            
    return Base,table



#Computes the canonical (Duquenne-Guigues) basis of a context
def NextClosureDG(context):
    table = []
    
    if len(context) > 3:
        context,table = multi2Bi(context)
    Implis = []
    A = logicalClosure(set([]),Implis)
    while len(A) < context[1]:
        B = Intent(Extent(A,context),context)
        if A != B:
            Implis.append([A,B])
        A = NextDG(A, Implis, context[2])
    return Implis,table



#Builds the neighbouring graph of a set of concepts (inclusion on the last n-1 components)
#Naive algorithm
def buildNeighbouringRelation(concepts):
    Edges = []
    
    for C in concepts:
        Candidates = []
        for D in concepts:
            if C != D:
                if subsetConcepts(C,D):
                    minimal = True
                    for i in range(len(Candidates)):
                        if subsetConcepts(Candidates[i],D):
                            minimal = False
                        else:
                            if subsetConcepts(D,Candidates[i]):
                                Candidates.pop(i)
                                i = i-1
                    if minimal:
                        Candidates.append(D)
        for D in Candidates:
            Edges.append([C,D])
            
    return Edges
    
    
#Computes an association rules base of the context
def associationRules(context):
    R = []
    Concepts = concepts(context)
    Neighbours = buildNeighbouringRelation(Concepts)
    for N in Neighbours:
        R.append([N[0][1],N[1][1],len(N[1][0])/len(N[0][0])])
    return R


#Computes the concepts that introduce elements of a particular dimension
def introducersDimension(context,dimension):
    R = []
    for e in range(context[dimension+1]):
        contS = sliceContext(context,e,dimension)
        concS = concepts(contS)
        for C in concS:
            Supp = support(C,context,dimension)
            C.insert(dimension,Supp)
            
            #check whether C is already in R and add if not
            oui = True
            for r in R:
                pareils = True
                for x in range(len(r)):
                    if set(r[x]) != set(C[x]):
                        pareils = False
                if pareils:
                    oui = False
            if oui:
                R.append(C)
            
            
    return list(R)


#Computes all the introducer concepts
def allIntroducers(context):
    nbDim = len(context)-1
    R = []
    for i in range(nbDim):
        I = introducersDimension(context,i)
        
        R2 = copy.deepcopy(R)
        for C in I:
            oui = True
            for r in R2:
                pareils = True
                for x in range(len(r)):
                    if set(r[x]) != set(C[x]):
                        pareils = False
                if pareils:
                    oui = False
            if oui:
                R.append(C)
    return R




'''
HubRCA
'''

def writeConcept(c,names):
    S = '['
    for comp in range(len(c)):
        S += '['
        for x in c[comp]:
            S += names[comp][x]
        S+= ']'
    S += ']'
    return S


#contextFamily: list of contexts (the first dimension of those contexts is the Object dimension)
#elementNames: true name of elements in the contexts of the contextFamily, of the form [[[c1_dim1_name1,c1_dim1,name2],[c1_dim2,name1]],[[c2_dim1,name1],[c2_dim2,name1],[c2_dim3,name1]]]
#relations: dictionary relation_name => [[x1,y1],[x2,y2],[x3,y3]]
#strategy: list of quadruples (lists) of the form [relation_name,source_context_id,target_context_id,quantificator] with quantificator = 0 for \exists and 1 for \forall (the id of a context is its index in the contextFamily)
#depth: number of iterations
def HubRCA(contextFamily,elementNames,relations,strategy,depth):
    #rajouter les \circlearrowleft (comme dernier élément d'une dimension)
    CF = copy.copy(contextFamily)
    CF2 = []
    idCont = 0
    for context in CF:
        for size in range(len(context)):
            if size > 1:
                context = list(context)
                context[size] += 1
                elementNames[idCont][size-1] += ["Disj"]
                newCroix = []
                for croix in context[0]:
                    nCroix = copy.copy(croix)
                    nCroix[size-1] = context[size] -1
                    ajout = True
                    for cr in newCroix:
                        if nCroix == cr:
                            ajout = False
                    if ajout:
                        newCroix += [nCroix]
                context[0] += newCroix
                context = tuple(context)
                CF2 += [context]
        idCont += 1
                
    CF = CF2
    

    iteration = 0
    while iteration < depth:
        for [name,source,target,quant] in strategy:
            conceptsTarget = concepts(CF[target])
            #création des attributs relationnels
            attributeNames = []
            for c in conceptsTarget:
                if quant == 0:
                    nomAttribut = "exists."+name+"."+str(writeConcept(c,elementNames[target]))
                else:
                    nomAttribut = "forall."+name+"."+str(writeConcept(c,elementNames[target]))
                attributeNames += [nomAttribut]
            attributeNames += ["Disj"]
            #ajout d'une nouvelle dimension
            CF[source] += (len(conceptsTarget)+1,)
            elementNames[source] += [attributeNames]
            
            #ajout des nouvelles croix
            newCroix = []
            for croix in CF[source][0]:
                newCroix += [croix+[len(attributeNames)-1]]
                for att in range(len(conceptsTarget)):
                    targs = set([tar for [x,tar] in relations[name] if x == croix[0]])
                    if quant == 0:
                        if len(targs) > 0 and not targs.isdisjoint(set(conceptsTarget[att][0])):
                            ajout = True
                            for cr in newCroix:
                                if croix+[att] == cr:
                                    ajout = False
                            if ajout:
                                newCroix += [croix+[att]]
                    else:
                        if len(targs) > 0 and targs.issubset(set(conceptsTarget[att][0])):
                            ajout = True
                            for cr in newCroix:
                                if croix+[att] == cr:
                                    ajout = False
                            if ajout:
                                newCroix += [croix+[att]]
            CF[source] = list(CF[source])
            CF[source][0] = newCroix
            CF[source] = tuple(CF[source])

        iteration += 1

    return [concepts(conc) for conc in CF]
