import re
import numpy as np
# import GDataWorks



#opens the given file and returns the lines of the file as an array
#where each row is a line and each line is made into a vector
#where the strings of the line are an entry in the row vector except the last which is the car name
#uses the clean line method below
#row vector is in the form
# 0         1            2            3         4          5             6         7       8
#[mpg,  cylinders,  displacement, horsepower, weight, acceelration, model year, origin, car name]
def DataCleaner(filename):

    f = open(filename, 'r')

    #set up and array for the lines in the file
    lines = []


    for line in f:

        #make sure it is a full line
        if( len(line) < 9):
            continue
        else:
            lines.append(CleanLine(line))

    #return the lines of the file as an array
    return lines

#Take a line from a file
#expands the tabs into spaces, splits the line by white space up to the car name(index 8)
#and removes all white space
def CleanLine(line):

    line = line.expandtabs()

    retLine = line.split(" ", 37)

    #count how many empty strings need to be removed
    numtogo = retLine.count("")

    #remove the empty strings
    for i in range(numtogo):
        retLine.remove('')

    #remove the new line and extra quote marks
    idx = len(retLine)-1
    retLine[idx] = retLine[idx].strip('\n')
    retLine[idx] = retLine[idx].strip('\"')

    return retLine


#returns a the given column of the given array
#as a vector(list)
#replaces ? with a zero
def GetCol(array, col):

    retvec = []
    badData = []

    #move through the rows of the array and grab the
    #entries at the given column
    for row in range(len(array)):
        entry = array[row][col]

        #if there is not bad data at this entry
        #add it to the return vector
        if entry != '?':
            retvec.append(array[row][col])
        #otherwise add a string version of a zero
        #and store the row where it was
        else:
            #print("found bad data")
            #print("at row " + str(row))
            retvec.append(str(0))
            badData.append(row)

    return retvec, badData




#Turn data array of strings into a dictionary keyed on the name of the car
#with values of the index in the array where that car name occurs
def makeCarDatabase(array):

    retDic = {}
    count = 0
    for idx in range( len(array) ):
        #grab the car name
        carname = array[idx][8]

        #print("the car is " + carname)
        #if the car is in the the map
        #add the current index into its values
        if carname in retDic:
            retDic[carname].append(idx)
        #otherwise create an entry into the map keyed on this carname
        #with a value of the current index in the array where this car occurs
        else:
            nlist = [idx]

            retDic[carname] = nlist

    return retDic
#basically does a transpose operation to make
#rows into what used to be the columns to make a
#rows the different attributes
#uses the GetCol vector which replaces ? with a zero
def makeColVector(array):

    colVecs = []


    #go through each columen except the last one
    for col in range(len(array[0])-1):

        #print("getting column: "+ str(col))

        colvec, badData = GetCol(array, col)
        if len(badData) > 0:
            pass
            #print("There was bad data at col "+str(col))
            #print(badData)
        colVecs.append(colvec)

    return colVecs


#will average a given vector distregarding 0 entries
#takes a column vector
#replaces ? markes with zero's
def MissingDataAverager(vector):

    sum = 0
    sub = 0
    fix = []
    amount = len(vector)

    print("there are " + str(amount)+ " items ")

    for i in range(amount):

        #grab the value as a float
        val = float(vector[i])
        #print("val is "+str(val))

        #if the value is zero ignore it
        #and remember where bad data is
        #by adding index to fix array
        if val == 0:
            sub += 1
            fix.append(i)
        #otherwise sum it
        else:
            sum += val

    print("the sub amount is " + str(sub) + " or " + str(len(fix)) )

    amount = amount - sub

    print("the new amount is " + str(amount))

    #calculate adjusted mean
    fixedmean = sum/amount

    print("the sub set mean is  "+str(fixedmean))

    #go through old array and fix the bad data
    #by replacing with the fixed mean
    #the fix list contains the indexs of the entrys that need to be fixed
    for entry in fix:
        vector[entry] = str(fixedmean)
    return vector, fixedmean, fix

#will replace bad data points with an averaged data point
#takes the data array that has entries to be fixed, the column
#in that array, the fix array containing thro row that needs to be fixed,
#and the fixed value to be added which is the average of the useable data
def FixBadDataAVG(dataArray, col, fixArray, fixedval):

    for entry in fixArray:
        dataArray[entry][col] = str(fixedval)

    return dataArray


#maks X array and Y array for multiple linear regression
def MakeXYarray(dataArray, badDataVal):

    #result array called Y
    Yarray = []

    #input value array called X
    Xarray = []

    #move through rows of data array
    for row in dataArray:

        #grab mpg or output value for this row
        Yarray.append(float(row[0]))
        xlist = []

        #append a 1 where the mpg value was(index 0)
        xlist.append(1.0)

        #move from column 1 to columen 7 to exclude the mpg and the carname repectively
        for i in range(1,8):
            fnum = row[i]
            #if we find some bad data replace it with the bad data value
            if fnum == '?':
                #fnum = '104.46938775510205'
                 fnum = badDataVal
            xlist.append(float(fnum))

        Xarray.append(xlist)

    return Xarray, Yarray










########################################################################################################
########################################################################################################

#used to help find a certain attributed
attribs = {"mpg": 0,
           "cylinders": 1,
           "displacement": 2,
           "horsepower": 3,
           "weight": 4,
           "acceleration": 5,
           "model year": 6,
           "origin": 7,
           "car name": 8}

#Open the car data file and process the file into the data array
dataArray = DataCleaner("CarData.txt")

#print(GDataWorks.FindBadDataPoints(dataArray, '?'))
print("the length is: " + str(len(dataArray)))

#print original data array
#print(dataArray)

'''
#strip out the x(attributes/independent vars) and y(dependent/MPG)
Xarry, Yarry = MakeXYarray(dataArray)
'''

'''
print(Xarry)
print("length of x " + str(len(Xarry))+ "\n")
print(Yarry)
print("length of Y " + str(len(Yarry))+ "\n")
'''


'''
#turn the arrays into np array for some math
X = np.array(Xarry, dtype=np.float64)
Y = np.array(Yarry, dtype=np.float64)
#print("X is..............")
#print(X)
'''

'''
#get the transpose of X
Xtranspose = np.transpose(X)
'''

'''
print("XT is..............")
print(Xtranspose)
print("Y is..............")
print(Y)
'''

'''
#get the (dot)product of Xtranspose and X
XTX = np.dot(Xtranspose, X)
'''

'''
print("XTX")
print(XTX)
'''


'''
#Get the inverse of of XTX
invXTX = np.linalg.inv(XTX)
'''


'''
print(invXTX)
'''


'''
#get the product of the inverse of XTX and Xtranspose
XTXinvXT = np.dot(invXTX, Xtranspose)
'''

'''
#get the product of the above and the independent var vector
#which is w or the parameter matrix
W = np.dot(XTXinvXT, Y)
'''


'''
print("W.....................................")
print(W)
'''


#sample = X[0]
#print(sample)


#test = np.dot(W,sample)

#print("Test..........")
#print(test)

#print( makeColVector(dataArray))

#print(GetCol(dataArray, 0))

#create a vector for each attribute
#will also find bad data points by making them zeros

'''
AttribVec = makeColVector(dataArray)
'''


'''
print("mpg :")
print(AttribVec[0])

print("cylinder: ")
print(AttribVec[1])

print("displacement: ")
print(AttribVec[2])
'''
#print("horsepower: ")
#print(AttribVec[3])
'''
print("weight: ")
print(AttribVec[4])

print("acceleration: ")
print(AttribVec[5])

print("model year: ")
print(AttribVec[6])

print("origin: ")
print(AttribVec[7])
'''

'''
#create a car data base
#stores names of cars and where in the data array they can be found
CarDB = makeCarDatabase(dataArray)
print("\n")
print(CarDB)
print("\n")
'''


#print(CarDB['ford pinto'])
#print(AttribVec[3][112])

'''
print(AttribVec[3][32])
print(AttribVec[3][126])
print(AttribVec[3][330])
print(AttribVec[3][336])
print(AttribVec[3][354])
print(AttribVec[3][374])
'''


#dependent variable
'''
print("the length of the mpg array is "+ str(len(AttribVec[0])))
mpgArray = np.array(AttribVec[0], dtype=np.float64)
mpgAvg = np.mean(mpgArray)
################################################################
'''

'''
cylinderArray = np.array(AttribVec[1], dtype=np.int64)
cyAvg = np.mean(cylinderArray)
cySTD = np.std(cylinderArray)

disArray = np.array(AttribVec[2], dtype=np.float64)
disAvg = np.mean(disArray)
disSTD = np.std(disArray)

#fix the horse power values by subing the mean for missing values
AttribVec[3] ,fixval, fixarray= MissingDataAverager(AttribVec[3])
print(AttribVec[3])
print(fixval)
print(fixarray)

#fix the bad data points by replacding with average value
fixAvgDataArray = FixBadDataAVG(dataArray, 3, fixarray, fixval)
hpArray = np.array(AttribVec[3], dtype=np.float64)
hpAvg = np.mean(hpArray)
hpSTD = np.std(hpArray)
'''

'''
print(fixAvgDataArray)
print("\n")
print(AttribVec[3][32])
print(AttribVec[3][126])
print(AttribVec[3][330])
print(AttribVec[3][336])
print(AttribVec[3][354])
print(AttribVec[3][374])
'''
'''
weightArray = np.array(AttribVec[4], dtype=np.float64)
weightAvg = np.mean(weightArray)
weightSTD = np.std(weightArray)

accelArray = np.array(AttribVec[5], dtype=np.float64)
accelAvg = np.mean(accelArray)
accelSTD = np.std(accelArray)

modelYearArray = np.array(AttribVec[6], dtype=np.int64)
modelYearAvg = np.mean(modelYearArray)
modelYearSTD = np.std(modelYearArray)

originArray = np.array(AttribVec[7], dtype=np.int64)
originAvg = np.mean(originArray)
originSTD = np.std(originArray)

print("mpg_avg            cyavg             disAvg             hpAvg              WAvg              accelAvg           Myr               Org")
print(mpgAvg, cyAvg, disAvg, hpAvg, weightAvg, accelAvg, modelYearAvg, originAvg)


print("mpg_std            cystd             disstd             hpstd              Wstd              accelstd            MYrstd          Orgstd")
print(mpgAvg, cySTD*cySTD, disSTD*disSTD, hpSTD*hpSTD, weightSTD*weightSTD, accelSTD*accelSTD, modelYearSTD*modelYearSTD, originSTD*originSTD)
#print(originArray[0:4])


test, verify, validate, Ytest, Yver, Yvali = GDataWorks.DataSpliter(fixAvgDataArray, 3, 0)

print("Test: ")
print(len(test))
print(test)
print("YTest: ")
print(Ytest)

print("Verify: ")
print(len(verify))
print(verify)
print("Yver: ")
print(Yver)

print("Validate: ")
print(len(validate))
print(validate)
print("Vali: ")
print(Yvali)

meanArray = GDataWorks.GmakeMeanArray(fixAvgDataArray)

print("mean array ")
print(meanArray)



#perform Multiple linear regression
WparamsT = GDataWorks.GMulLinReg(test, Ytest)
WparamsVer = GDataWorks.GMulLinReg(verify, Yver)
WparamsVal = GDataWorks.GMulLinReg(validate, Yvali)

print(WparamsT.size)
print(WparamsVer.size)
print(WparamsVal.size)

GdataVer = GDataWorks.TestModel(verify, WparamsT)
GdataTest = GDataWorks.TestModel(test, WparamsVer)
GdataVali = GDataWorks.TestModel(validate, WparamsT)
print(GdataTest.size)
print(GdataVer.size)
print(GdataVali.size)

RSET = GDataWorks.CalculateMSE(GdataTest, np.array(Ytest, dtype=np.float64) )
RSEVer = GDataWorks.CalculateMSE(GdataVer, np.array(Yver, dtype=np.float64) )
RSEVal = GDataWorks.CalculateMSE(GdataVali, np.array(Yvali, dtype=np.float64) )

BGdata = GDataWorks.TestModel(X,W)
BRSE = GDataWorks.CalculateMSE(BGdata, Y)
print(RSET)
print(RSEVer)
print(RSEVal)
print(BRSE)

BestRse, increment , testsize = GDataWorks.GTrainer(fixAvgDataArray)


print("Coefficient of Det.   incr    testsize")
print(BestRse, increment, testsize)
'''

#print(dataArray)
