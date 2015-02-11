
def binP(N, p, x1, x2):
    p = float(p)
    q = p/(1-p)
    k = 0.0
    v = 1.0
    s = 0.0
    tot = 0.0

    while(k<=N):
            tot += v
            if(k >= x1 and k <= x2):
                    s += v
            if(tot > 10**30):
                    s = s/10**30
                    tot = tot/10**30
                    v = v/10**30
            k += 1
            v = v*q*(N+1-k)/k
    return s/tot

def calcBin(vx, vN, vCL = 95):
    '''
    Calculate the exact confidence interval for a binomial proportion

    Usage:
    >>> calcBin(13,100)
    (0.07107391357421874, 0.21204372406005856)
    >>> calcBin(4,7)
    (0.18405151367187494, 0.9010086059570312)
    '''
    vx = float(vx)
    vN = float(vN)
    #Set the confidence bounds
    vTU = (100 - float(vCL))/2
    vTL = vTU

    vP = vx/vN
    if(vx==0):
            dl = 0.0
    else:
            v = vP/2
            vsL = 0
            vsH = vP
            p = vTL/100

            while((vsH-vsL) > 10**-5):
                    if(binP(vN, v, vx, vN) > p):
                            vsH = v
                            v = (vsL+v)/2
                    else:
                            vsL = v
                            v = (v+vsH)/2
            dl = v

    if(vx==vN):
            ul = 1.0
    else:
            v = (1+vP)/2
            vsL =vP
            vsH = 1
            p = vTU/100
            while((vsH-vsL) > 10**-5):
                    if(binP(vN, v, 0, vx) < p):
                            vsH = v
                            v = (vsL+v)/2
                    else:
                            vsL = v
                            v = (v+vsH)/2
            ul = v
    return (dl, ul)

import operator
__author__ = 'zashk_000'
import csv

#row counter
rownum=0
#dictioanry to hold the map
d = {}

#index of the column to be used in the hash
colName = 4
#limit of number of rows to be scanned, -1 means all
maxRownum = -1
#threshold on the number of trials of an ad to be ranked in sucesss analysis, -1 means no threshold
MinRecords = -1
#40428967

with open('C:/Work/UofA/Job Search/Resume/Submission2/Mediative/Assignment/train.csv', 'r') as f:
    reader = csv.reader(f)

    #print the file header
    for x in range(0,24):
        print(x,end=',')
    print('\n',end='')
    print(next(reader))

    #parse the csv file one row at a time
    for row in reader:
        rownum+=1
        if rownum==maxRownum:
            break
        #show progress
        if rownum%1000000==0:
            print(rownum)
        #the current row's target variable
        currentKey = (row[colName])
        #check if this row has a hit
        isHit = int(row[1])
        if not (isHit==0 or isHit==1):
            print("error: invalid hit value=", isHit)

        #update dictionary to add the new key if not already existing
        if currentKey not in d:
            #list to hold miss and hit count
            d[currentKey]=[0,0]
        #update the miss or hit of the currentKey accordingly
        d[currentKey][isHit]+=1

dicRates=d
for k in dicRates:
    trials=dicRates[k][0]+dicRates[k][1]
    #first entry in the list is hits
    dicRates[k][0]=dicRates[k][1]
    #second entry is the total number of records
    dicRates[k][1]=trials
    #third entry is the sample hitrate
    dicRates[k].append(dicRates[k][0]/trials)
    #fourth entry is the confidence lower bound on the hitrate
    if trials>MinRecords:
        dicRates[k].append(calcBin(dicRates[k][0], 1+trials, vCL = 99))
    else:
        dicRates[k].append((-dicRates[k][0]/trials,-dicRates[k][0]/trials))

print("#distinct members="+str(len(d)))
print("#rows parsed="+str(rownum))

i=1
#show the categories with highest hitrate bounds on top
for key, value in sorted(dicRates.items(), key=lambda e: e[1][3],reverse=True):
       if (value[1])>MinRecords:
           print("#",i,"= ",key, ": ", value)
           i+=1

