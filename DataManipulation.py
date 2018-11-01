import numpy as np
import Regression
from numpy.core.multiarray import ndarray
from matplotlib.pyplot import *

# ----------------------------------------Data manipulation and searching-------------------------------


# splits x data and y data into training and validation sets
# based on splitval array which holds percentages
def dos_data_splitter(xdata, ydata, splitval_array):
    training_data = []
    validation_data = []
    y_training = []
    y_validation = []

    train_limit = int(len(xdata)*splitval_array[0])
    val_limit = len(xdata)

    # used to pick random observations for each data set
    random_selection = np.random.choice(len(xdata), len(ydata), replace=False)

    # grab training data set
    for idx in range(0, train_limit):
        row = random_selection[idx]
        training_data.append(xdata[row])
        y_training.append(ydata[row])

    # grab validation data set
    for idx in range(train_limit, val_limit):
        row = random_selection[idx]
        validation_data.append(xdata[row])
        y_validation.append(ydata[row])
    return training_data, validation_data, y_training, y_validation, random_selection


def tres_data_splitter(xdata, ydata, splitval_array):
    training_data = list()
    validation_data = list()
    test_data = list()

    y_training = list()
    y_validation = list()
    y_test = list()

    train_limit = int(len(xdata)*splitval_array[0])
    val_limit = int(len(xdata)*splitval_array[1]) + train_limit
    test_limit = len(xdata)

    # used to pick random observations for each data set
    random_selection = np.random.choice(len(xdata), len(ydata), replace=False)

    # grab training data set
    for idx in range(0, train_limit):
        row = random_selection[idx]
        training_data.append(xdata[row])
        y_training.append(ydata[row])
    # grab validation data set
    for idx in range(train_limit, val_limit):
        # for idx in range(train_limit, val_limit):
        row = random_selection[idx]
        validation_data.append(xdata[row])
        y_validation.append(ydata[row])
    for idx in range(val_limit, test_limit):
        row = random_selection[idx]
        test_data.append(xdata[row])
        y_test.append(ydata[row])
    return training_data, validation_data, y_training, y_validation, test_data, y_test, random_selection


# finds bad data points and returns a map
# keyed on the column and with a value of a list of the
# rows where the bad data is located
def find_col_bad_data(dataarray, badsig):
    retdic = {}
    for col in range(len(dataarray[0])):
            for row in range(len(dataarray)):
                if dataarray[row][col] == badsig:
                    if col in retdic:
                        retdic[col].append(row)
                    else:
                        rowlist = [row]
                        retdic[col] = rowlist
    return retdic


def replace_item(data_array, bad_data_dictionary, value_array):

    count: int = 0
    for col in bad_data_dictionary:
        for row in bad_data_dictionary[col]:
            data_array[row][col] = value_array[count]
        count += 1
    return data_array


# replaces bad data with the given value
def replace_bad_data_vec(data: list, baddic: dict, vec: list) -> list:
    for entry in baddic:
        badlist = baddic[entry]
        for idx in range(len(badlist)):
            row = badlist[idx]
            data[row][entry] = float(vec[idx])
    return data.copy()


# will return an X array full of independent variables, and a Y array of the dependant
# variables
def x_y_getter(array, y_col):
    y = column_getter(array, y_col)

    front = [array[i][0:y_col] for i in range(0, len(array))]
    back = [array[i][y_col + 1:] for i in range(0, len(array))]

    # chunk1 = front[0] + endr[0]
    # chunk2 = hlf1[1] + endr[1]
    # chunk = [chunk1] + [chunk2]

    x = [[1] + front[0] + back[0]]

    for idx in range(1, len(array)):
        x += [[1] + front[idx] + back[idx]]

    return x, y


# removes selected data found in bad_list
def remove_row(array, bad_list):
    count = 0
    for entry in bad_list:
        del array[entry - count]
        count += 1
    return array


# removes the column col from the data array
def remove_col(array, col):
    for row in range(0, len(array)):
        del array[row][col]
    return array


# gets the column col from the data array
def column_getter(array, col):
    y2d = [array[i][col:col+1] for i in range(0, len(array))]
    # print(format('\n'))
    # print('Y2d')
    # print(Y2d)
    # print(format('\n'))
    retlist = []
    for row in y2d:
        retlist.append(row[0])
    return retlist


# converts data array elements to either floats or ints depending on con_dis array
# will also replace unknown data signified with bad_sig with a zero
def convert_strings_float_int(data_array, bad_sig,  con_dis):
    for row in range(len(data_array)):
        # print(row)
        for col in range(len(data_array[0])):
            val = data_array[row][col]
            if val == bad_sig:
                data_array[row][col] = float(0)
                # del data_array[row]
                # count += 1
            else:
                if con_dis[col] == 1:
                    data_array[row][col] = int(data_array[row][col])
                else:
                    data_array[row][col] = float(data_array[row][col])

    return data_array


# --------------------------------------------------------------------------------------------------------


# ------------------------------------------------Imputation functions------------------------------------


def discard_imputation(data_array, cont_dis, cols_rmv, bad_sig, ind_col):
    baddatdic = find_col_bad_data(data_array.copy(), bad_sig)

    # remove the column for car name
    for col in cols_rmv:
        data_array = remove_col(list(data_array), col)

    # Convert strings to numerical values
    # using the continuous/discrete array to turn the value into a float or an int respectively
    data_array = convert_strings_float_int(list(data_array), bad_sig, cont_dis)
    # remove the rows with bad data
    for entry in baddatdic:
        data_array = remove_row(list(data_array), baddatdic[entry])
    ret_data, stat_array, x, y, x_norm, y_norm = get_fixed_data_stats_x_y_xn_yn(data_array, cont_dis, ind_col)

    return ret_data, stat_array, x, y, x_norm, y_norm


def average_imputation(data_array, cont_dis, cols_rmv, bad_sig, ind_col):
    bad_dat_dic = find_col_bad_data(data_array.copy(), bad_sig)

    # print(bad_dat_dic)

    value_array = list()

    # remove the column for car name
    for col in cols_rmv:
        data_array = remove_col(list(data_array), col)

    data_array = convert_strings_float_int(list(data_array), bad_sig, cont_dis)

    dat_a = list(data_array)

    for row in bad_dat_dic:
        # calculate the average of the HorsePowerData
        # Get the horse power column
        #
        hp_array = column_getter(list(dat_a), row)

        # make a copy of it so we can average it up
        hp_averager = list(hp_array)

        # remove the rows with bad data points
        hp_averager = remove_row(hp_averager, bad_dat_dic[row])

        # calculate the average of the Horse Power attribute
        # and use it to replace missing data
        hp_mean = np.mean(np.array(hp_averager, dtype=np.float), dtype=np.float)

        value_array.append(hp_mean)

    # add the average in place of missing data
    data_array = replace_item(list(dat_a), bad_dat_dic, value_array)

    for avg in value_array:
        print('avg: ' + str(avg))

    return get_fixed_data_stats_x_y_xn_yn(data_array, cont_dis, ind_col)


# performs linear regression imputation on data array
def linear_regression_imputation(data_array, cont_dis, cols_rmv, bad_sig, ind_col):


    bad_dat_dic = find_col_bad_data(data_array.copy(), bad_sig)

    # remove the column for car name
    for col in cols_rmv:
        data_array = remove_col(list(data_array), col)

    data_array = convert_strings_float_int(list(data_array), bad_sig, cont_dis)

    dat_a = list(data_array)

    # x = column_getter(dat_a, )

    # remove the rows found in the list at key 3 in the dictionary
    d_a_known = remove_row(list(dat_a), bad_dat_dic[3])

    x = column_getter(d_a_known, 4)

    # print('hopefully the weight array is:')
    # print(x)
    # print(format('\n'))

    # split the data into a independent array(X) and the dependent array(y)
    # where Y is the horse power column
    # through the find first method found that weight (3)leads to the best mse error
    x_a_lr_i, y_a_lr_i = x_y_getter(list(d_a_known), 3)

    # ------------------------Find the best column
    # Use the find_first method to find the column that leads to the lowest mean square error (mse)
    # and return the column number (min_col), the minimum mean square error (min_mse), and the best column
    # it self
    # min_col, min_mse, best_col = Regression.find_first(list(x_a_lr_i), list(y_a_lr_i), list([.60, .40]))
    #print(format('\n'))
    #print('The minimum column is {:d}'.format(min_col[0]))
    #print(format('\n'))

    # hp_array = DataProcessor.column_getter(list(y_a_lr_i), attribute_label_array.index('Horse Power'))
    hp_array = list(y_a_lr_i)

    # solve for the parameters
    # w_imp = Regression.multi_linear_regressor(x_a_lr_i, hp_array)

    w_imp = Regression.linear_calculation_for_w(x, hp_array)

    # use the parameter array to calculate values for the missing data points
    #rt = Regression.getlinregmissingdata(list(data_array), bad_dat_dic, w_imp)

    rt = Regression.reg_lin_regresser(x, w_imp)

    figure(1)
    title('Weight vs. Horse Power')
    plot(x, rt, 'r--', label='weight vs regression')
    plot(x, y_a_lr_i, 'o', label='c label')
    legend(['regression data', 'raw data'])
    show()

    # replace missing values in original data array with the estimates found through
    # regression
    imputation_data = replace_bad_data_vec(list(data_array), bad_dat_dic, rt)

    return get_fixed_data_stats_x_y_xn_yn(imputation_data, cont_dis, ind_col)


# -------------------------------Data Analysis-----------------------------------------------

def get_fixed_data_stats_x_y_xn_yn(data_a, cont_dis, ind_col):
    # get x and y matrices
    x, y = x_y_getter(list(data_a), ind_col)

    smu, std, min_a, max_a = get_basic_stats(data_a, cont_dis)

    stat_array = [smu, std, min_a, max_a]

    ret_data = list()

    for row in data_a:
        ret_data.append(list(row))

    # print('data array in func')
    # print(data_a)

    orig_data = data_a[:]

    norm_dat = normalize_data(orig_data.copy(), smu, std, min_a, max_a, cont_dis)

    x_n, y_n = x_y_getter(list(norm_dat), ind_col)

    # print('orig array in func')
    # print(ret_data)
    # print('data array in func')
    # print(data_a)
    # print('normalized data array in func')
    # print(norm_dat)

    return ret_data, stat_array, x, y, x_n, y_n


# returns two lists one contains the min values of the columns,
# and the other returns the max values
def max_min_array_getter(attrib_data):
    min_array = []
    max_array = []

    for col in range(len(attrib_data[0])):
        attrib = np.array(column_getter(attrib_data, col), dtype=np.float)

        min_array.append(np.amin(attrib))
        max_array.append(np.amax(attrib))

    return min_array, max_array


# returns the z-normalized value of x
# takes as arguments the mean, and standard deviation
def z_number(x, mu, sigma):
    return (x - mu)/sigma


# returns the normalized version of x
def normalization(x, x_min, x_max):
    return (x - x_min)/(x_max - x_min)


# creates a normalized version of attrib data array
# con_dis indicates which values are continuous or discrete
def normalize_data(attrib_d, mean_l, sigma_l, min_l, max_l, con_dis):
    col_end = len(attrib_d[0])
    row_end = len(attrib_d)

    ret_array = list(attrib_d[:])

    for c in range(0, col_end):

        for r in range(0, row_end):

            if con_dis[c] == 0:
                ret_array[r][c] = z_number(attrib_d[r][c], mean_l[c], sigma_l[c])
            elif con_dis[c] == 1:
                ret_array[r][c] = normalization(attrib_d[r][c], min_l[c], max_l[c])

    return ret_array



def z_norm_col(y, mu, std):
    tmp_l = []
    for row in y:
        diffy = row - mu
        tmp_l.append(diffy/std)
    return tmp_l


# performs z normalization on the given attribute array
def z_normalization(attrib_data, mean_array, std_array):
    col_end = len(attrib_data[0])
    z_norm_vals = list(attrib_data)
    tmp_list = []

    for col in range(0, col_end):
        # attrib = np.array(GetColumn(attrib_data, col), dtype=np.float)
        attrib = np.array(column_getter(attrib_data, col), dtype=np.float)

        # print('attrib for column: ' + str(col))
        # print(attrib)
        tmp_list.clear()
        # sum = 0
        for row in range(len(attrib)):
            dif = (attrib[row] - mean_array[col])
            # print('dif at row: ' + str(row))
            # print(dif)
            # print('mean at col: ' + str(col) + ' is ')
            # print(mean_array[col])
            if std_array[col] == 0:
                tmp_list.append(dif/mean_array[col])
            else:
                tmp_list.append(dif/std_array[col])

        for row in range(len(z_norm_vals)):
            z_norm_vals[row][col] = tmp_list[row]

    return list(z_norm_vals)


# returns the sample mean of the attributes in the given array
# returning a int for discrete values and a float for continuous values
# uses the con_dis array to tell the difference
def sample_mean_array(array, con_dis):
    smu = []

    limit = len(array[0])

    for col in range(0, limit):
        if con_dis[col] == 0:
            smu.append(np.mean(np.array(column_getter(array, col), dtype=np.float), dtype=float))
        elif con_dis[col] == 1:
            smu.append(np.mean(np.array(column_getter(array, col), dtype=np.int), dtype=np.int))
    return smu


# returns the sample standard deveation of the attributes in the given array
def sample_std_array(attribdata):
    end = len(attribdata[0])
    ssig2 = []
    discrete_vals = [1, 6, 7]
    for col in range(0, end):
        if col in discrete_vals:
            attrib = np.array(column_getter(attribdata, col), dtype=np.int)
            ssig2.append(int(np.std(attrib, dtype=np.int)))
        else:
            attrib = np.array(column_getter(attribdata, col), dtype=np.float)
            ssig2.append((np.std(attrib, dtype=np.float)))
    return list(ssig2)


def quartiles_array(data):

    q_array = []

    for col in range(data[0]-1):
        attrib = column_getter(data, col)
        lq, uq, md, medn = quartiles(attrib)
        q_list = [lq, uq, md, medn]
        q_array.append(q_list)
    return q_array


def quartiles(attrib_data):
    sorted_points = sorted(attrib_data)
    # 2. divide the data set in two halves
    mid = len(sorted_points) / 2

    a_median: ndarray = np.median(attrib_data)

    if len(sorted_points) % 2 == 0:
        # even
        lower_q = np.median(sorted_points[:mid])
        upper_q = np.median(sorted_points[mid:])
    else:
        # odd
        lower_q = np.median(sorted_points[:mid])  # same as even
        upper_q = np.median(sorted_points[mid + 1:])

    return lower_q, upper_q, mid, a_median


# will calculate and return the basic stats of a data set
# i.e.
# sample mean
# sample standard deviation
# min attribute array
# max attribute array
def get_basic_stats(data_array, continuous_discrete):

    smu = sample_mean_array(data_array, continuous_discrete)

    std = sample_std_array(data_array)

    min_a, max_a = max_min_array_getter(data_array)

    return smu, std, min_a, max_a

# ------------------------------------------------------------------------------------------------------
