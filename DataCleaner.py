

# opens the given file and returns the lines of the file as an array
# where each row is a line and each line is made into a vector
# where the strings of the line are an entry in the row vector except the last which is the car name
# uses the clean line method below
# row vector is in the form
# 0         1            2            3         4          5             6         7       8
# [mpg,  cylinders,  displacement, horsepower, weight, acceelration, model year, origin, car name]
def data_cleaner(filename):

    f = open(filename, 'r')

    # set up and array for the lines in the file
    lines = []

    for line in f:

        # make sure it is a full line
        if len(line) < 9:
            continue
        else:
            lines.append(clean_line(line))

    # return the lines of the file as an array
    return lines


# Take a line from a file
# expands the tabs into spaces, splits the line by white space up to the car name(index 8)
# and removes all white space
def clean_line(line):

    line = line.expandtabs()

    ret_line = line.split(" ", 37)

    # count how many empty strings need to be removed
    num_to_go = ret_line.count("")

    # remove the empty strings
    for i in range(num_to_go):
        ret_line.remove('')

    # remove the new line and extra quote marks
    idx = len(ret_line)-1
    ret_line[idx] = ret_line[idx].strip('\n')
    ret_line[idx] = ret_line[idx].strip('\"')

    return ret_line
