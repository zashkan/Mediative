
import random
import csv

colName = 0
maxRownum = -1
MinRecords = -1
#the sample rate is 1 in every #outOf records
outOf=10

with open('C:/Work/UofA/Job Search/Resume/Submission2/Mediative/Assignment/train.csv', 'r') as f:
    with open('C:/Work/UofA/Job Search/Resume/Submission2/Mediative/Assignment/sample.csv', 'w', newline='') as csvfile:
        rownum=0
        reader = csv.reader(f)
        filedNames = next(reader)
        sampleWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        sampleWriter.writerow(filedNames)

        for row in reader:
            rownum+=1
            if rownum==maxRownum:
                break
            if outOf==random.randint(1, outOf):
                sampleWriter.writerow(row)

        print("#rows parsed="+str(rownum))



