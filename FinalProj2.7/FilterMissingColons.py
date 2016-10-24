import os
import re
import csv

def getFullPath(fileName, isOutput=False):
    if (isOutput):
        dir = os.path.join(os.getcwd(), 'Data', 'FetchedData', 'FinalData', fileName)
    else:
        dir = os.path.join(os.getcwd(), 'Data', 'FetchedData', fileName)
    return dir

def getMissingId(Index, InputArray):
    CheckPrevious = False
    while InputArray[Index] is not None:
        Index = Index - 1
        splitValues= InputArray[Index].split(':')
        CheckPrevious = re.match(r'\d', splitValues[0]) is not None
        if CheckPrevious:
            return Index

f = open(getFullPath('tweet.NON_SARCASM.all.id.TRAIN.csv', True), 'rb')
data = f.read()
DataArray = data.split('\n')
lenDataArray = len(DataArray)
i=0

while (i < lenDataArray):
    separateValues = DataArray[i].split(':')
    lineNumber = str(i+1) + ') '
    tweet = re.match(r'\d', separateValues[0])
    if tweet is None:
        havingId = getMissingId(i, DataArray)
        DataArray[havingId]=DataArray[havingId].replace("\r",'.')
        DataArray[havingId] += " " + DataArray[i]
        DataArray.remove(DataArray[i])
        lenDataArray=lenDataArray-1
    else:
        #print lineNumber , DataArray[i]
        i=i+1

modifiedList=[]

for index in range(0 , lenDataArray):
    #lineNumber = str(index+1) + ') '
    SplitString = DataArray[index].replace('\r','').replace('\n','').split(":")
    #myfile.write(DataArray[index])
    tempString=''
    if(len(SplitString)>2):
        shortCounter=0
        for i in SplitString:
            if(shortCounter==1):
                tempString += i + ' '
            if(shortCounter==0):
                shortCounter=shortCounter+1
                shortStr = SplitString[0]+':'
        modifiedList.insert(index , (shortStr + tempString))
    else:
        modifiedList.insert(index , (SplitString[0] + ':' + SplitString[1]))

with open("D:\File.csv","w") as myfile:
    lis=[line.split(':') for line in modifiedList]
    for i,x in lis:
        myfile.write(i + ' ' + x + "\n")