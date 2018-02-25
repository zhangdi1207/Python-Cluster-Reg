import matplotlib.pyplot as plt
import random
import numpy as np

def initData(N,vo):
    # N is the classify of data
    # v is the variance's order of the magnitudes
    data=[]
    oriCen=[]
    for i in range(N):
        x=random.random()*2*N
        y=random.random()*2*N
        v=random.randrange(1,3)*vo
        oriCen.append([x,y])
        for j in range(random.randint(1000,2000)):
            dotx,doty=random.normalvariate(x,v),random.normalvariate(y,v)
            if dotx*dotx + doty*doty < 16*N*N:
                data.append([dotx,doty])
    return np.array(data),np.array(oriCen)

def drawData(data,label,center,oriCen):
    colorList=['r','y','g','c','m','tan','b','k']
    markList=['.','+']
    data=np.r_[data,center]
    data=np.r_[data,oriCen]
    centerLabel=[colorList[-1] for i in range(len(center))]
    oriCenLabel=[colorList[-2] for i in range(len(center))]
    colorLabel =[colorList[i] for i in label]
    colorLabel.extend(centerLabel)
    colorLabel.extend(oriCenLabel)
    #print(label,colorLabel)
    plt.scatter(data[:,0],data[:,1],c=colorLabel,marker=markList[0])
    #plt.scatter(center[:,0],center[:,1],c='k',marker=markList[1])
    plt.show()

def dis(d1,d2):
    distance=0
    for i in range(len(d1)):
        distance+=(d1[i]-d2[i])**2
    return distance**0.5

def meanShift(data,N=3,r=0.5,minNum=10):
    # N is the number of divided part(original)
    # r is the radius
    # minNum is the min number of dot in every final cycle(r,final center)
    feature = len(data[0])
    x=[]
    for i in range(feature):
        tempList=data[:,0].tolist()
        x.append([(N-j)*min(tempList)/N+j*max(tempList)/N for j in range(N)])
    initCenter=[[]] # initial Center , some one has no data
    oriCen=[] # del no data center

    for i in range(feature):
        initCenter=[[j,]+k for j in x[i] for k in initCenter]
    for i in range(len(initCenter)):
        for j in range(len(data)):
            if dis(initCenter[i],data[j])<r:
                oriCen.append(initCenter[i])
                break
    label=[-1 for i in range(len(data))]
    for i in range(len(data)):
        tempDisList=[dis(j,data[i]) for j in oriCen]
        minDis = min(tempDisList)
        if minDis <= r:
            label[i] = tempDisList.index(min(tempDisList))
    label=np.array(label)
    for i in range(len(oriCen)):
        oriCen[i]=data[label==i].mean(axis=0)
    print('11111',type(oriCen),'11222',type(data))
    return oriCen,label

data,oriCen=initData(3,0.1)
center,label = meanShift(data)
print(center)
plt.scatter(center[:,0],center[:,1])

