# Created by: Gerald Jones
# Purpose: This will hopefully use linear regression to model how
#         the number of cylinders, displacement, horsepower, weight,
#         acceleration, model year, and origin of a car can be used with
#         linear regression techniques to predict mpg. This one discards
#         observations with bad data
import DataCleaner
import Regression

Imputations_options = ['0', '1', '2', '3', '4', '5']
imputation_methods = ['Discard Imputation', 'Average Imputation', 'Linear Regression Imputation',
                      'discard with forward selection', 'Average Imputation with forward selection',
                      'Linear Regression Imputation with forward selection']

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

# print(str.format('Using ' + error_methods[int(error)] + '\n'))

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

# used to remove car names from data array
cols_rmv = [8]

# represents the data split (traingin, validation)
size = [.75, .25]


split_selection = list()

runs = 15
for x in range(0, runs):
    split_selection.append(size)

print('Number of Runs: ', runs)
print("Data Split: ", split_selection[0])

# get the data using data cleaner
# returns a 2D array where rows are observations and columns
# are attributes of a specific observations
data_array = DataCleaner.data_cleaner("CarData.txt")

# used to do Linear Regression.
# Arguments are:
#               data_array: The data array created with DataCleaner
#               imputation: The users choice of imputation
#               cont_dis: The array that represents which cols/attributes are continuous or discrete(0,1)
#               cols_rmv: The columns the user would like to be removed from the data set here it is the car_name
#               bad data signal: This will be used to determine if and what data points are missing
#               split_selection: Array controlling how many tests are run and the split between test and validation sets
Regression.perform_regression(list(data_array), imputation, cont_dis, cols_rmv, '?', 0, split_selection)
