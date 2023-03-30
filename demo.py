from sklearn.cluster import KMeans
from sklearn import cluster, datasets, metrics
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import random
import operator

f = open( "data.txt", 'r' )     
array = np.loadtxt('data.txt',dtype=int) #資料
print(array)
arraycluster = np.zeros(75,dtype=int) #分群
center = np.zeros(shape=[1,4],dtype=int) #中心點
sse = np.zeros(10, dtype=int)
def EucliDist(x, y):
    return np.sqrt(sum(np.power((x - y), 2)))     #歐式距離

def FindCluster(array, arraycluster, center, clustertimes ) :  
    for i in range(75) :
        cluster = 0         # 預設為第1群的
        minDist = EucliDist(array[i], center[0])   # 預設離第1群最近
        for Cindex in range(clustertimes) :
            if ( EucliDist( array[i], center[Cindex] ) < minDist ): 
                minDist = EucliDist(array[i], center[Cindex])
                cluster = Cindex                         # 設為第幾群

            arraycluster[i] = cluster

def FindnewCluster(array, arraycluster, center, clustertimes):
    precenter = center
    for clusterIndex in range(clustertimes) :
        clusterX = 0 
        clusterY = 0 
        clusterA = 0 
        clusterB = 0
        index = 0  
        for Arrayindex in range(75) :
            if( arraycluster[Arrayindex] == clusterIndex ) :
                clusterX = array[Arrayindex][0] + clusterX
                clusterY = array[Arrayindex][1] + clusterY
                clusterA = array[Arrayindex][2] + clusterA
                clusterB = array[Arrayindex][3] + clusterB
                index = index + 1
        
        center[clusterIndex][0] = clusterX / index
        center[clusterIndex][1] = clusterY / index
        center[clusterIndex][2] = clusterA / index
        center[clusterIndex][3] = clusterB / index
        if( ( precenter == center ).all() ):
            return True
        precenter = center


def getSse( array, arraycluster, center, clustertimes, sse ):
    for i in range( clustertimes ):
        for j in range(75) :
            if( arraycluster[j] == i ) :
                sse[i] =  sse[i] + np.square(EucliDist(array[j],center[i]))


for clustertimes in range(1 ,11) :
    center = np.zeros(shape=[clustertimes,4],dtype=int)
    for i in range(clustertimes) :  # 設定中心點
        centerIndex = random.randint(0,74)
        center[i] = array[centerIndex]
    FindCluster( array, arraycluster, center, clustertimes )
    if( FindnewCluster( array, arraycluster, center, clustertimes) ):
        pass
    getSse(array,arraycluster,center,clustertimes,sse)
        
getSse(array,arraycluster,center,clustertimes,sse)
txt=open('C:/Users/lab602/Desktop/test/machine learning/result.txt','w+')
for i in range(75) :
    print( array[i] , "Cluster : ",arraycluster[i], file=txt )
    print("\n" , file=txt)
txt.close()

plt.plot( range(1,11), sse, 'o-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.savefig("C:/Users/lab602/Desktop/test/machine learning/K.jpg")
plt.show()
print(sse)
