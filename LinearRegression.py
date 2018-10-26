# Created by: Gerald Jones
# Purpose: This will hopefully use linear regression to model how
#         the number of cylinders, displacement, horsepower, weight,
#         acceleration, model year, and origin of a car can be used with
#         linear regression techniques to predict mpg. This one discards
#         observations with bad data

# import numpy as np
# from matplotlib.pyplot import *
# import GDataWorks
import DataCleaner
import DataManipulation
import Regression

Imputations_options = ['0', '1', '2', '3', '4', '5']
imputation_methods = ['Discard Imputation', 'Average Imputation', 'Linear Regression Imputation',
                      'discard with forward selection', 'Average Imputation with forward selection',
                      'Linear Regression Imputation with forward selection']

'''
split_options = [[.60, .40],    # 0
                 [.75, .25],    # 1
                 [.50, .50],    # 2
                 [.40, .60],    # 3
                 [.65, .35]]    # 4
'''
# num_split_options = ['0', '1', '2', '3', '4']

while True:
    print(format('Imputation options: '))
    print(format("0: Use Discard Imputation               3: Discard Imputation with forward selection"))
    print(format("1: Use Average Imputation               4: Average Imputation with forward selection"))
    print(format("2: Use Linear regression Imputation     5: Linear Regression Imputation with forward selection"))
    imputation = input("Chose a Imputation Method: ")
    if imputation in Imputations_options:
        break
    else:
        print("No option for " + str(imputation))
        print(format('\n'))


print(str.format('Using ' + imputation_methods[int(imputation)] + '\n'))

'''
while True:
    print(str.format('Training vs. Validation Split Size Options:'))
    print(str.format("0: " + str(split_options[0])))
    print(str.format("1: " + str(split_options[1])))
    print(str.format("2: " + str(split_options[2])))
    print(str.format("3: " + str(split_options[3])))
    print(str.format("3: " + str(split_options[4])))
    split_decision = (input("Chose a Split for Training set vs. Validation set size: "))
    if split_decision in num_split_options:
        break
    else:
        print("No option for " + split_decision)
        print(format('\n'))

print('Training vs. Validation split: ', split_options[int(split_decision)])
'''

'''
run_size = 10

while True:
    run_size = int(input("Give me the number of runs you want to do: "))
    if run_size in range(1, 101):
        break
    else:
        print('Run size must be between 10 and 100 inclusive')
        print(format('\n'))

print('Run size: ', run_size)
'''

# print(str.format('Using ' + error_methods[int(error)] + '\n'))

'''
attribute_label_array = ['mpg',           # 0
                         'Cylinders',     # 1
                         'Displacement',  # 2
                         'Horse Power',   # 3
                         'Weight',        # 4
                         'Acceleration',  # 5
                         'Model Year',    # 6
                         'Origin',        # 7
                         'Car Type']      # 8
'''

# usded to signify which attributes are continuous (0) or discrete (1)
cont_dis = [0,    # 0 mpg
            1,    # 1 cylinders
            0,    # 2 displacement
            0,    # 3 horse power
            0,    # 4 weight
            0,    # 5 acceleration
            1,    # 6 model year
            1,    # 7 Origin
            1, ]  # 8 car type number

# decided to remove car names
cols_rmv = [8]

# the below arrays are used to run 20 runs with the sam separation(training, validation)
# the different arrays attempt to see if there is an optimal seperation

# Various sizes of the training and validation sets
#size = split_options[int(split_decision)]
size = [.75, .25]

# Will hold arrays of the various training and validation sizes

# determines the size of the run arrays

split_selection = list()

limit = 15
for x in range(0, limit):
    split_selection.append(size)

print('Number of Runs: ', limit )
print("Data Split: ", split_selection[0])

# get the data using data cleaner
# returns a 2D array where rows are observations and columns
# are attributes of a specific observations
dataarray = DataCleaner.DataCleaner("CarData.txt")

Regression.perform_regression(list(dataarray), imputation, cont_dis, cols_rmv, '?', 0, split_selection)

