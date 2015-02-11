
import operator
__author__ = 'zashk_000'
import math
import csv

colName = 0
maxRownum = -1
MinRecords = -1
#since one dictionary on the whole add_ids does not fit in memory
#look at #dateDayChunk of days in each scan of the file
dateDayChunk=4

for dateDayChunkCounter in range(0,math.ceil(10/dateDayChunk)):
    with open('C:/Work/UofA/Job Search/Resume/Submission2/Mediative/Assignment/train.csv', 'r') as f:
        rownum=0
        monthRowCounter=[0,0,0,0]
        #list of four dictionaries
        dList = [{}, {}, {}, {}]
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            rownum+=1
            if rownum==maxRownum:
                break
            #the position of the current records date in the list of dictionaries.
            dictIndex=int(row[2][0:6])-141021-dateDayChunkCounter*dateDayChunk

            currentKey = int(row[colName])
            if dictIndex<dateDayChunk and dictIndex>=0:
                dictIndex=0
                monthRowCounter[dictIndex]+=1
                if currentKey not in dList[dictIndex]:
                    dList[dictIndex][currentKey]=1

        print("#rows parsed="+str(rownum))
        print("#rows in month="+str(monthRowCounter))
        for i in range(0,dateDayChunk):
            print("len dict ", str(141021+dateDayChunkCounter*dateDayChunk+i),len(dList[i]))
        print("all combined= distict are ",len(dList[0])," out of ",sum(monthRowCounter))


