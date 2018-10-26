import numpy as np
# for storing dictionaries
import operator
import DataManipulation

# ----------------------------------------------Regression Functions----------------------------------------------


# performs multiple linear regrsion on the x and y data
# and returns the generated parameter vector W
def multi_linear_regressor(x_data, y_data):
    x = np.array(x_data, dtype=np.float)
    y = np.array(y_data, dtype=np.float)
    x_transpose = np.transpose(x)
    xtx = np.dot(x_transpose, x)
    xtx_inv = np.linalg.inv(xtx)
    xtx_inv_xt = np.dot(xtx_inv, x_transpose)
    w = np.dot(xtx_inv_xt, y)
    return w


# does linear regression imputataion on the
# original / regular data
def getlinregmissingdata(regdata, baddic, w):
    r = []
    for entry in baddic:
        dlist = baddic[entry]
        for row in dlist:
            x = list()
            x.append(1)
            for col in range(len(regdata[0])):
                if col != entry:
                    x.append(regdata[row][col])
            xnp = np.array(x, dtype=np.float64)
            wnp = np.array(w, dtype=np.float64)
            r.append(np.dot(xnp, wnp))
    return r


# uses linear regression to generate a slope(m) and intercept(b) value
# for a line approximating the data
# def reg_lin_regression_MSR(X, Y):
def reg_lin_regression_msr(x, y, split):
    # split the data
    train_limit = int(len(x) * split[0])
    val_limit = len(x)

    training_data = []
    validation_data = []
    y_training = []
    y_validation = []

    # grab training sets
    for idx in range(0, train_limit):
        training_data.append(x[idx])
        y_training.append(y[idx])

    # grab validation data sets
    for row in range(train_limit, val_limit):
        validation_data.append(x[row])
        y_validation.append(y[row])

    # get attribute weights
    w = linear_calculation_for_w(training_data, y_training)
    b = w[0]
    m = w[1]
    yg = list()
    for idx in range(len(validation_data)):
        val = m*validation_data[idx] + b
        yg.append(val)
    mse = mean_square_error(yg, y_validation)
    return m, b, x, y, yg, mse


# calculates the attributes weights array (w)
# using the matrix equation
def linear_calculation_for_w(x, y):
    xsum = sum(x)
    ysum = sum(y)

    xy = [a * b for a, b in zip(x, y)]

    xx = [a * b for a, b in zip(x, x)]

    xxsum = sum(xx)

    xysum = sum(xy)

    n = len(x)

    a = [[n, xsum],
         [xsum, xxsum]]

    y = [ysum,
         xysum]

    anp = np.array(a)

    anpinv = np.linalg.inv(anp)

    ynp = np.array(y)

    w = np.dot(anpinv, ynp)

    return w


# get a set of y's using x_data and parameters w
def get_r_data(x_data, w):
    r = []

    wnp = np.array(w, dtype=np.float64)
    for row in range(len(x_data)):
        x_observation = list()
        # x_observation.append(1)
        for col in range(len(x_data[0])):
            x_observation.append(x_data[row][col])
        r.append(np.dot(np.array(x_observation, dtype=np.float64), wnp))
    return r

# ----------------------------------------------------------------------------------------------------------------


# -----------------------------------------------Collect parameters-----------------------------------------------
# Splits the given data into training and validation sets
# uses the test set to calculate a list of W values (parameters w_list)
# a list of training sets (tr_l), y values for that training set (y_tr_l)
# a list of validation sets, and there y values (val_l and y_val_l respectively)
# returns those in a list in the order: [w_list, tr_l, y_tr_list, val_l, y_val_l]]
#                                          0      1       2         3       4
def collect_parameters2(x_d, y_d, split_a):
    w_list = list()
    tr_l = list()
    y_tr_l = list()
    val_l = list()
    y_val_l = list()

    for x in range(len(split_a)):
        tr, val, y_tr, y_val, rand = DataManipulation.dos_data_splitter(x_d, y_d, split_a[x])

        # get w from training data
        w_list.append(multi_linear_regressor(tr, y_tr))
        tr_l.append(tr)
        y_tr_l.append(y_tr)
        val_l.append(val)
        y_val_l.append(y_val)

    return w_list, tr_l, y_tr_l, val_l, y_val_l
# ---------------------------------------------------------------------------------------------------------------


# --------------------------------------Testing Functions--------------------------------------------------------
# Runs tests on all given data (dat_l) using the parameters (w_l)
# and uses the dependent data (y_dat_l) to calculate the COD
# for each parameter and storing the average COD for that parameter
# Returns: tet_tuple:  a list of tuples containing the lndex in w_l, and the the best average ocd generated by that w
#          W_tuple: a list of tuples containing the lndex in w_l, and the the best average ocd generated by that w
#          w_ret_l: a list containing the top w's that had the best Cod, will be used to validation test
#          sorted_cods: a sorted version of all cod's generated in the order of largest to smallest
#          cods_best: a list of the best  avg cod's
#          the_best_cod: the highest cod generated
def test_data_set_cod_a(w_l, dat_l, y_dat_l):

    cods_best = list()
    test_dic = {}
    ret_dic = {}
    avg_cod = [0]
    best_avg: int = 0
    w_ret_l = []
    cod_l = list()

    for i in range(len(w_l)):
        current_cod_l = list()
        # test the randomized sameple
        for idx in range(len(dat_l)):
            gmodel = get_r_data(dat_l[idx], w_l[i])
            cod = np.around(calculate_cod(gmodel, y_dat_l[idx]), 12)
            # will collect cods for this w
            current_cod_l.append(cod)

            # will collect all cods generated
            cod_l.append(cod)

        # store the average cod for current W
        avg_cod[0] = np.mean(current_cod_l, dtype=np.float)

        cods_best.append(avg_cod[0])
        # if the current average is better than the stored best store it
        if best_avg < avg_cod[0] and avg_cod[0] > 0 and avg_cod[0] <= 1:
            # cods_best.append(avg_cod[0])
            best_avg = avg_cod[0]
            test_dic[i] = np.around(avg_cod[0], 12)

        ret_dic[i] = np.around(avg_cod[0], 12)

    sorted_cods = sorted(cod_l, reverse=True)

    the_best_cod = sorted_cods[0]

    # will hold the best only the best cods sorted from best to worst
    ret_tuple = sorted(test_dic.items(), key=operator.itemgetter(1), reverse=True)

    # holds all cod averages for all w's sorted from best to worst
    w_tuple = sorted(ret_dic.items(), key=operator.itemgetter(1), reverse=True)

    for idx in range(len(w_tuple)):
        w_ret_l.append(w_l[w_tuple[idx][0]])

    return ret_tuple, w_tuple, w_ret_l, sorted_cods, sorted(cods_best, reverse=True), the_best_cod


# Runs tests on all given data (dat_l) using the parameters (w_l)
# and uses the dependent data (y_dat_l) to calculate the Least Square Estimate(lse)
# for each parameter and storing the average lse for that parameter
# Returns: tet_tuple:  a list of tuples containing the lndex in w_l, and the the best average ocd generated by that w
#          W_tuple: a list of tuples containing the lndex in w_l, and the the best average ocd generated by that w
#          w_ret_l: a list containing the top w's that had the best lse, will be used to validation test
#          sorted_cods: a sorted version of all cod's generated in the order of largest to smallest
#          cods_best: a list of the best cods
#          the_best_cod: the highest cod generated
def test_data_set_lse_a(w_l, dat_l, y_dat_l):

    dat_lse = list()
    lse_best = list()
    test_dic = {}
    ret_dic = {}
    avg_lse = [0]
    best_avg = 10000
    w_ret_l = []
    lse_l = list()

    for i in range(len(w_l)):

        current_lse = list()
        # test the randomized sameple
        for idx in range(len(dat_l)):
            gmodel = get_r_data(dat_l[idx], w_l[i])
            lse = np.around(least_squares_estimate(gmodel, y_dat_l[idx]), 4)
            dat_lse.append(lse)
            current_lse.append(lse)
            lse_l.append(lse)

        avg_lse[0] = np.mean(current_lse, dtype=np.float)

        lse_best.append(avg_lse[0])

        if best_avg > avg_lse[0]:
            best_avg = avg_lse[0]
            test_dic[i] = np.around(avg_lse[0], 4)

        ret_dic[i] = np.around(avg_lse[0], 4)

    sorted_lses = sorted(lse_l, reverse=False)

    the_best_lse = sorted_lses[0]

    ret_tuple = sorted(test_dic.items(), key=operator.itemgetter(1), reverse=False)
    w_tuple = sorted(ret_dic.items(), key=operator.itemgetter(1), reverse=False)

    for idx in range(len(w_tuple)):
        w_ret_l.append(w_l[w_tuple[idx][0]])

    return ret_tuple, w_tuple, w_ret_l, sorted_lses, sorted(lse_best, reverse=False), the_best_lse


# Runs tests on all given data (dat_l) using the parameters (w_l)
# and uses the dependent data (y_dat_l) to calculate the Mean Square Error (mse)
# for each parameter and storing the average Lse for that parameter
# Returns: tet_tuple:  a list of tuples containing the lndex in w_l, and the the best average mse generated by that w
#          W_tuple: a list of tuples containing the lndex in w_l, and the the best average mse generated by that w
#          w_ret_l: a list containing the top w's that had the best mse, will be used to validation test
#          sorted_mses: a sorted version of all mse's generated in the order of largest to smallest
#          cods_best: a list of the best mses
#          the_best_mse: the highest cod generated
def test_data_set_mse_a(w_l, dat_l, y_dat_l):

    dat_mse = list()
    mse_best = list()
    test_dic = {}
    ret_dic = {}
    avg_mse = [0]
    best_avg = 1000
    w_ret_l = []
    mse_l = list()

    for i in range(len(w_l)):
        current_mse = list()
        # test the randomized sameple
        for idx in range(len(dat_l)):
            gmodel = get_r_data(dat_l[idx], w_l[i])
            mse = np.around(mean_square_error(gmodel, y_dat_l[idx]), 4)
            dat_mse.append(mse)
            current_mse.append(mse)
            mse_l.append(mse)

        avg_mse[0] = np.mean(current_mse, dtype=np.float)
        mse_best.append(avg_mse[0])

        if best_avg > avg_mse[0]:
            best_avg = avg_mse[0]
            test_dic[i] = np.around(avg_mse[0], 4)

        ret_dic[i] = np.around(avg_mse[0], 4)

    sorted_mses = sorted(mse_l, reverse=False)

    the_best_mse = sorted_mses[0]

    ret_tuple = sorted(test_dic.items(), key=operator.itemgetter(1), reverse=False)
    w_tuple = sorted(ret_dic.items(), key=operator.itemgetter(1), reverse=False)

    for idx in range(len(w_tuple)):
        w_ret_l.append(w_l[w_tuple[idx][0]])

    return ret_tuple, w_tuple, w_ret_l, sorted_mses, sorted(mse_best, reverse=False), the_best_mse


# ----------------------------------------------------------------------------------------------------------------


# ---------------------------------------Training Functions-------------------------------------------------------
# will attempt to train the data using the objects in
# a list of parameters:
#  values(w), training data, y for training data, validation data, y for the validation data
def train_model_cod2(param_tr_val_a):
    # a list of parmeter vectors
    w_list = param_tr_val_a[0]

    # a list of training data sets
    tr_l = param_tr_val_a[1]
    # the dependent variables of the training sets
    y_tr_l = param_tr_val_a[2]

    # a list of validation data sets
    val_l = param_tr_val_a[3]
    # the dependent variables of the training sets
    y_val_l = param_tr_val_a[4]

    # ret_tuple,    w_tuple,     w_ret_l, sorted cods,  all the best cods, the best cod
    ret_tuple_trn, w_tuple_trn, tr_w_l, cod_tr, cods_best_tr, t_b_cod_t = test_data_set_cod_a(w_list, tr_l, y_tr_l)
    ret_tuple_val, w_tuple_val, val_w_l, cod_val, cods_best_val, t_b_cod_v = test_data_set_cod_a(tr_w_l, val_l, y_val_l)

    # the below no longer due anything and should be removed
    val_avg_cod_avg_b = list()
    tr_avg_cod_avg_b = list()

    ret_val = [[cod_tr, cods_best_tr, t_b_cod_t, ret_tuple_trn[0][0], cods_best_tr[0]],
               [cod_val, cods_best_val, t_b_cod_v, ret_tuple_val[0][0], cods_best_val[0]],
               [tr_avg_cod_avg_b, val_avg_cod_avg_b]]

    return ret_val


# will attempt to train the data using the objects in
# a list of parameter values(w), training data, y for training data
# validation data, y for the validation data
def train_model_lse2(param_tr_val_a):
    w_list = param_tr_val_a[0]

    tr_l = param_tr_val_a[1]
    y_tr_l = param_tr_val_a[2]

    val_l = param_tr_val_a[3]
    y_val_l = param_tr_val_a[4]

    # ret_tuple,    w_tuple,     w_ret_l, sorted cods,  all the best cods, the best cod
    ret_tuple_trn, w_tuple_trn, tr_w_l, lse_tr, lses_best_tr, t_b_lse_t = test_data_set_lse_a(w_list, tr_l, y_tr_l)
    ret_tuple_val, w_tuple_val, val_w_l, lse_val, lses_best_val, t_b_lse_v = test_data_set_lse_a(tr_w_l, val_l, y_val_l)

    val_avg_lse_avg_b = list()
    tr_avg_lse_avg_b = list()

    ret_val = [[lse_tr, lses_best_tr, t_b_lse_t, ret_tuple_trn[0][0], lses_best_tr[0]],
               [lse_val, lses_best_val, t_b_lse_v, ret_tuple_val[0][0], lses_best_val[0]],
               [tr_avg_lse_avg_b, val_avg_lse_avg_b]]


    return ret_val


# will attempt to train the data using the objects in
# a list of parameter values(w), training data, y for training data
# validation data, y for the validation data
def train_model_mse2(param_tr_val_a):
    w_list = param_tr_val_a[0]

    tr_l = param_tr_val_a[1]
    y_tr_l = param_tr_val_a[2]

    val_l = param_tr_val_a[3]
    y_val_l = param_tr_val_a[4]

    # ret_tuple,    w_tuple,     w_ret_l, sorted cods,  all the best cods, the best cod
    ret_tuple_trn, w_tuple_trn, tr_w_l, mse_tr, mses_best_tr, t_b_mse_t = test_data_set_mse_a(w_list, tr_l, y_tr_l)
    ret_tuple_val, w_tuple_val, val_w_l, mse_val, mses_best_val, t_b_mse_v = test_data_set_mse_a(tr_w_l, val_l, y_val_l)

    val_avg_mse_avg_b = list()
    tr_avg_mse_avg_b = list()

    ret_val = [[mse_tr, mses_best_tr, t_b_mse_t, ret_tuple_trn[0][0], mses_best_tr[0]],
               [mse_val, mses_best_val, t_b_mse_v, ret_tuple_val[0][0], mses_best_val[0]],
               [tr_avg_mse_avg_b, val_avg_mse_avg_b]]

    return ret_val


# ------------------------------------------------Error Functions----------------------------------------------

# will perform all error test check and return the results
def er_t(x, y, x_n, y_n, split_array):
    cod_result, n_cod_result = test_cod_error(list(x), list(y), list(x_n), list(y_n), list(split_array))
    lse_result, n_lse_result = test_lse_error(list(x), list(y), list(x_n), list(y_n), list(split_array))
    mse_result, n_mse_result = test_mse_error(list(x), list(y), list(x_n), list(y_n), list(split_array))
    return cod_result, n_cod_result, lse_result, n_lse_result, mse_result, n_mse_result


def test_cod_error(x, y, x_n, y_n, split_array):

    w_list, tr_l, y_tr_l, val_l, y_val_l = collect_parameters2(x, y, split_array)
    param_tr_val_a = [w_list, tr_l, y_tr_l, val_l, y_val_l]
    ret_list = train_model_cod2(param_tr_val_a)

    w_list_n, tr_l_n, y_tr_l_n, val_l_n, y_val_l_n = collect_parameters2(x_n, y_n, split_array)
    param_tr_val_a_n = [w_list_n, tr_l_n, y_tr_l_n, val_l_n, y_val_l_n]
    ret_list2 = train_model_cod2(param_tr_val_a_n)

    return ret_list, ret_list2


def test_lse_error(x, y, x_n, y_n, split_array):

    w_list, tr_l, y_tr_l, val_l, y_val_l = collect_parameters2(x, y, split_array)
    param_tr_val_a = [w_list, tr_l, y_tr_l, val_l, y_val_l]
    ret_list = train_model_lse2(param_tr_val_a)

    w_list_n, tr_l_n, y_tr_l_n, val_l_n, y_val_l_n = collect_parameters2(x_n, y_n, split_array)
    param_tr_val_a_n = [w_list_n, tr_l_n, y_tr_l_n, val_l_n, y_val_l_n]
    ret_list2 = train_model_lse2(param_tr_val_a_n)

    return ret_list, ret_list2


def test_mse_error(x, y, x_n, y_n, split_array):

    w_list, tr_l, y_tr_l, val_l, y_val_l = collect_parameters2(x, y, split_array)
    param_tr_val_a = [w_list, tr_l, y_tr_l, val_l, y_val_l]
    ret_list = train_model_mse2(param_tr_val_a)

    w_list_n, tr_l_n, y_tr_l_n, val_l_n, y_val_l_n = collect_parameters2(x_n, y_n, split_array)
    param_tr_val_a_n = [w_list_n, tr_l_n, y_tr_l_n, val_l_n, y_val_l_n]
    ret_list2 = train_model_mse2(param_tr_val_a_n)

    return ret_list, ret_list2


# calculates the Mean Square Error
def calculate_cod(g_model, r_validate):

    r_mean = np.mean(r_validate)
    bottom = 0
    top = 0
    for idx in range(len(g_model)):
        top += np.power((r_validate[idx] - g_model[idx]), 2)
    for idx in range(len(r_validate)):
        bottom += np.power((r_validate[idx] - r_mean), 2)
    return 1 - top/bottom


# calculates the mean square error
def mean_square_error(d_array, yarray):
    n = len(d_array)
    difference_list = []
    for idx in range(n):
        diff = d_array[idx] - yarray[idx]
        difference_list.append(pow(diff, 2))
        # difference_list.append(np.absolute(diff))
    return np.mean(np.array(difference_list, dtype=np.float64))


# calculates the least squares estimate
def least_squares_estimate(d_array, y_array):
    n = len(d_array)
    summation = 0
    for idx in range(n):
        diff = d_array[idx] - y_array[idx]
        summation += np.power(diff, 2)
    return summation / 2

# --------------------------------------------------------------------------------------------------------------------


# -------------------------------------------Dimension Reduction------------------------------------------------------
# will use linear regression to find the first attribute
# to add to the F array for forward selection
# will split the data into training and validation sets
# according to split parameter
def find_first(x_data, y_data, split):
    col_size = len(x_data[0])
    min_mse = [10000]
    min_col = [10000]
    best_col = [0]
    for col in range(1, col_size):
        x_column = list(DataManipulation.column_getter(x_data, col))

        m, b, x, y, yg, mse = reg_lin_regression_msr(x_column, y_data, split)

        if mse < min_mse[0]:
            min_col[0] = col
            min_mse[0] = mse
            best_col[0] = list(x_column)

    return list(min_col), list(min_mse), list(best_col)


# attempts to do forward selection
def forward_selector_test(x_data, y_data, split):

    attribute_labels = ['mpg',           # 0
                        'Cylinders',     # 1
                        'Displacement',  # 2
                        'Horse Power',   # 3
                        'Weight',        # 4
                        'Acceleration',  # 5
                        'Model Year',    # 6
                        'Origin',        # 7
                        'Car Type']      # 8

    train_limit = int(len(x_data) * split[0])
    val_limit = len(x_data)

    nx = len(x_data)
    col_size = len(x_data[0])
    used_col = []

    cols_f = list()

    found = True

    addcol = [2000]

    mininmum_mse = [10000]

    f = list()

    # find the first variable  array to add to F as well its mean square error
    min_col, min_mse, best_col = find_first(x_data.copy(), y_data.copy(), split)

    print(y_data)

    print('First column')
    print(attribute_labels[min_col[0]])
    print(format("\n"))

    cols_f.append(min_col[0])

    # used to ignore column 1
    used_col.append(0)
    used_col.append(min_col[0])
    mininmum_mse[0] = min_mse[0]

    # set up F array
    for row in range(nx):
        flist = [1.0]
        f.append(flist)

    for row in range(nx):
        f[row].append(best_col[0][row])

    # while old_error > new_error:
    while found:
        found = False
        for col in range(1, col_size):
            if col not in used_col:
                f_tmp = f[:]

                # create a temp F array
                # each row of Ftmp contains a list
                # adds the current column
                for row in range(nx):
                    f_tmp[row].append(x_data[row][col])

                train = list()
                y_training = list()
                val = list()
                y_val = list()

                for row in range(0, train_limit):
                    train.append(list(f_tmp[row]))
                    y_training.append(y_data[row])

                for row in range(train_limit, val_limit):
                    val.append(list(f_tmp[row]))
                    y_val.append(y_data[row])

                # perform linear regression to get W params
                w_params = multi_linear_regressor(train, y_training)

                # use w to get some response data
                gmodel = get_r_data(val, w_params)

                # calculate the mean square error for this x column
                mse = mean_square_error(gmodel, y_val)
                for row in range(nx):
                    f_tmp[row].pop()

                diff = (mininmum_mse[0] - mse)/mininmum_mse[0]

                if mse < mininmum_mse[0] and diff > .10:
                    mininmum_mse[0] = mse
                    addcol[0] = col
                    found = True

        if not found:
            break
        else:
            for row in range(nx):
                f[row].append(x_data[row][addcol[0]])

            used_col.append(addcol[0])
            cols_f.append(addcol[0])
            if len(f) == col_size + 1:
                break
        print('using Attributes: ')
        for i in range(len(cols_f)):
            print(attribute_labels[cols_f[i]])

    return f, mininmum_mse[0], cols_f


# ------------------------------------Display functions-------------------------------------------------#

def show_results(imp_name, cod_r, lse_r, mse_r):

    b_t_c = np.around(cod_r[0][4], 2)
    b_t_l = np.around(lse_r[0][4], 2)
    b_t_m = np.around(mse_r[0][4], 2)

    b_v_c = np.around(cod_r[1][4], 2)
    b_v_l = np.around(lse_r[1][4], 2)
    b_v_m = np.around(mse_r[1][4], 2)

    print('Imputation type: ' + imp_name)
    print('--------------------------------------Best Training averages:----------------------------------------')
    print('                       Coefficient of Determination          Least Squares Error          Mean Square Error')
    print('Training: {:>28.2f} {:>35.2f} {:>26.2f}'.format(b_t_c, b_t_l, b_t_m))
    print('Validation: {:>26.2f} {:>35.2f} {:>26.2f}'.format(b_v_c, b_v_l, b_v_m))

    return


# ---------------------------------Linear Regression methods------------------------------------------


# perform regression with
def regression_discard(data_array, cont_dis, cols_rmv, sig, y_col, split_array):
    print('-----------------------------------')
    print('Using Discard Imputation')
    print('-----------------------------------')
    imp = 'Discard Imputation:'
    d_array, stat_a, x, y, x_n, y_n = DataManipulation.discard_imputation(list(data_array), cont_dis, cols_rmv, sig, y_col)

    cod_r, n_cod_r, lse_r, n_lse_r, mse_r, n_mse_r = er_t(list(x), list(y), list(x_n), list(y_n), split_array)

    print('Unnormalized Result: ')
    show_results(imp, cod_r, lse_r, mse_r)
    print('Normalized Result: ')
    show_results(imp, n_cod_r, n_lse_r, n_mse_r)
    return


# perfomre regression with
def regression_discard_fs(data_array, cont_dis, cols_rmv, sig, y_col, split_array):
    print('-----------------------------------')
    print('Using Discard Imputation with Forward Selection Dimension Reduction')
    print('-----------------------------------')
    imp = 'Discard Imputation:'
    d_array, stat_a, x, y, x_n, y_n = DataManipulation.discard_imputation(list(data_array), cont_dis, cols_rmv, sig,y_col)

    F, min_mse, cols_f = forward_selector_test(list(x), list(y), split_array[0])
    f_n, min_mse_n, cols_f_n = forward_selector_test(list(x_n), list(y_n), split_array[0])

    print('F is using ' + str(len(F[0]) - 1) + ' attributes')

    cod_r, n_cod_r, lse_r, n_lse_r, mse_r, n_mse_r = er_t(list(F), list(y), list(f_n), list(y_n), split_array)

    print('Unnormalized Result: ')
    show_results(imp, cod_r, lse_r, mse_r)
    print(format('\n'))
    print('Normalized Result: ')
    show_results(imp, n_cod_r, n_lse_r, n_mse_r)

    return


# perfomre regression with
def regression_average(data_array, cont_dis, cols_rmv, sig, y_col, split_array):
    print('-----------------------------------')
    print('Using Average Imputation:')
    print('-----------------------------------')

    imp = 'Average Imputation:'

    d_array, stat_a, x, y, x_n, y_n = DataManipulation.average_imputation(list(data_array), cont_dis, cols_rmv, sig, y_col)

    cod_r, n_cod_r, lse_r, n_lse_r, mse_r, n_mse_r = er_t(list(x), list(y), list(x_n), list(y_n), split_array)

    print('Unnormalized Data:')
    show_results(imp, cod_r, lse_r, mse_r)
    print('Normalized Data:')
    show_results(imp, n_cod_r, n_lse_r, n_mse_r)
    return


# perfomre regression with
def regression_average_fs(data_array, cont_dis, cols_rmv, sig, y_col, split_array):
    print('-----------------------------------')
    print('Using Average Imputation with Forward Felection Dimension Reduction')
    print('-----------------------------------')

    imp = 'Average Imputation:'

    d_array, stat_a, x, y, x_n, y_n = DataManipulation.average_imputation(list(data_array), cont_dis, cols_rmv, sig, y_col)

    F, min_mse, cols_f = forward_selector_test(list(x), list(y), split_array[0])
    f_n, min_mse_n, cols_f_n = forward_selector_test(list(x_n), list(y_n), split_array[0])

    print('F is using ' + str(len(F[0]) - 1) + ' attributes')
    print('F normalized is using ' + str(len(f_n[0]) - 1) + ' attributes')

    cod_r, n_cod_r, lse_r, n_lse_r, mse_r, n_mse_r = er_t(list(F), list(y), list(f_n), list(y_n), split_array)

    # show_results(imp, error, cod_result, lse_result, mse_result)
    print('Unnormalized Data:')
    show_results(imp, cod_r, lse_r, mse_r)
    print('Normalized Data:')
    show_results(imp, n_cod_r, n_lse_r, n_mse_r)

    return


# perfomre regression with
def regression_linear_regression(data_array, cont_dis, cls_rmv, sig, y_col, split_array):
    print('-----------------------------------')
    print('Using Linear Regression Imputation')
    print('-----------------------------------')

    imp = 'Linear Regression Imputation:'

    d_a, stat_a, x, y, x_n, y_n = DataManipulation.linear_regression_imputation(list(data_array), cont_dis, cls_rmv, sig, y_col)

    cod_r, n_cod_r, lse_r, n_lse_r, mse_r, n_mse_r = er_t(list(x), list(y), list(x_n), list(y_n), split_array)

    print('Unnormalized Data:')
    show_results(imp, cod_r, lse_r, mse_r)
    print('Normalized Data:')
    show_results(imp, n_cod_r, n_lse_r, n_mse_r)

    return


# perfomre regression with
def regression_linear_regression_fs(data_array, cont_dis, cls_rmv, sig, y_col, split_array):
    print('-----------------------------------')
    print('Using Linear Regression Imputation')
    print('-----------------------------------')

    imp = 'Linear Regression Imputation:'

    d_a, stat_a, x, y, x_n, y_n = DataManipulation.linear_regression_imputation(list(data_array), cont_dis, cls_rmv, sig, y_col)

    F, min_mse, cols_f = forward_selector_test(list(x), list(y), split_array[0])
    f_n, min_mse_n, cols_f_n = forward_selector_test(list(x_n), list(y_n), split_array[0])

    print('F is using ' + str(len(F[0]) - 1) + ' attributes')
    print('F normalized is using ' + str(len(f_n[0]) - 1) + ' attributes')

    cod_r, n_cod_r, lse_r, n_lse_r, mse_r, n_mse_r = er_t(list(F), list(y), list(f_n), list(y_n), split_array)

    print('Unnormalized Data:')
    show_results(imp, cod_r, lse_r, mse_r)
    print('Normalized Data:')
    show_results(imp, n_cod_r, n_lse_r, n_mse_r)

    return


# will perform the indicated imputation method and do a attempt to train
# the model using linear Regression
def perform_regression(data_a, imputation, cont_dis, cols_rmv, sig, y_col, split_array):
    # (data_array, cont_dis, cls_rmv, sig, y_col, split_array)

    if int(imputation) == 0:
        regression_discard(data_a, cont_dis, cols_rmv, sig, y_col, split_array)
    elif int(imputation) == 1:
        regression_average(data_a, cont_dis, cols_rmv, sig, y_col, split_array)
    elif int(imputation) == 2:
        regression_linear_regression(data_a, cont_dis, cols_rmv,sig, y_col, split_array)
    elif int(imputation) == 3:
        regression_discard_fs(data_a, cont_dis, cols_rmv, sig, y_col, split_array)
    elif int(imputation) == 4:
        regression_average_fs(data_a, cont_dis, cols_rmv, sig, y_col, split_array)
    elif int(imputation) == 5:
        regression_linear_regression_fs(data_a, cont_dis, cols_rmv, sig, y_col, split_array)

    return