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
        for j in range(random.randint(50,100)):
            dotx,doty=random.normalvariate(x,v),random.normalvariate(y,v)
            if dotx*dotx + doty*doty < 16*N*N:
                data.append([dotx,doty])
    return np.array(data),np.array(oriCen)

def drawData(data,label,center,oriCen):
    colorList=['r','c','g','b','m','tan','y','k']
    markList=['.','+']
    data=np.r_[data,center]
    data=np.r_[data,oriCen]
    centerLabel=[colorList[-1] for i in range(len(center))]
    oriCenLabel=[colorList[-2] for i in range(len(center))]
    colorLabel =[colorList[i] for i in label]
    colorLabel.extend(centerLabel)
    colorLabel.extend(oriCenLabel)
    plt.ion()
    plt.scatter(data[:,0],data[:,1],c=colorLabel,marker=markList[0])
    #plt.show()
    plt.pause(1.5)
    plt.close()

def dis(d1,d2):
    distance=0
    for i in range(len(d1)):
        distance+=(d1[i]-d2[i])**2
    return distance**0.5

def kMeans(data,k,iteration=50,tol=0.0001):
    center=np.array([[0.0,0.0] for i in range(k)])
    label=np.array([-1 for i in range(len(data))])
    changeMeth = random.randint(0,1)
    for i in range(k):
        if changeMeth==0:
            temp = sorted(data,key=lambda x:x[(i%(len(data[0])))//2],reverse=[0,1][i%2==0])[random.randint(0,len(data)-1)]
        else:
            temp = data[random.randint(0,len(data)-1)]
        if temp not in center:
            center[i] = temp
    err=tol*10.0
    it=0
    while(err>tol and it<iteration):
        it+=1
        for i in range(len(data)):
            disList=[]
            for j in range(k):
                disList.append(dis(data[i],center[j]))
            label[i] = disList.index(min(disList))
        errList=[0,]
        for i in range(k):
            if len(data[label==i])==0:
                return 0,0,0
            newCenter = data[label==i].mean(axis=0)
            errList.append(dis(newCenter,center[i]))
            center[i] = newCenter
        err=max(errList)
    disSum=0.0
    for i in range(k):
        for j in data[label==i]:
            disSum += dis(center[i],j)
    return label,center,disSum


def test(k,vo):
    data,oriCen=initData(k,vo)
    meanList=[]
    best=[[],[],np.inf]
    for i in range(5):
        temp = kMeans(data,k)
        if temp[2]==0:
            return
        if best[2] > temp[2]:
            best = temp
    label,center,disSum = best
    #np.savetxt("1.txt",data)
    drawData(data,label,center,oriCen)

for i in range(100):
    test(3,0.10)

