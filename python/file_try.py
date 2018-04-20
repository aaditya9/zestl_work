import csv
import statistics

# list1 = [1,2,3]
list1 = [{"abc":1},{"gef":2},{"minal":3},{"mayuri":7}]
reversed_list = list(reversed(list1))
print reversed_list



# infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/try.csv"

#************ statistics in python ***********#
# exlist = [2,6,8,5]
# x = statistics.mean(exlist)
# print x

#******* Read lines from file ******#
# read = open(infile , 'r').readlines()
# print read


#******* Append a file ***************************#
# newline = "\n Green vegitables are good for health"
# wfile = open(infile , 'a')
#
# wfile.write(newline)
# wfile.close()


#******* Writing to the file **********************#
# text = " Always Be Positive"
# wfile = open(infile , 'w')
#
# wfile.write(text)
# wfile.close()

#******* In this program we r reading Color from file and giving us date which is with that color *************#

# with open(infile , 'r') as f:
#     data = csv.reader(f)
#     colors = []
#     dates = []
#
#     for row in data:
#         # print row
#         color = row[3]
#         date = row[0]
#         colors.append(color)
#         dates.append(date)
#         print colors
#         print dates
#
#     try:
#
#         whatColor = input('What color do you wish to know the date of?:')
#         if whatColor in colors:
#             coldex = colors.index(whatColor)
#             theDate = dates[coldex]
#             print('The date of', whatColor, 'is:', theDate)
#         else:print "not found"
#     except Exception as e:
#         print e
#
#     print "code is running"

#****************************************#
    # rownum = 0
    # colnum = 0
    # for row in data:
    #     if rownum == 0:
    #         header = row
    #     else:
    #         colnum = 0
    #     for col in row:
    #         print '%-8s: % s' % (header[colnum], col)
    #     colnum = colnum + 1
    #
    #     rownum = rownum + 1

#***********************************************#
#*********** removing duplicates from file *********************#
# csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_users.csv"
# with open(csvfile, 'r') as f:
#     data = csv.reader(f, delimiter=',')
#     seen = set()
#     for data in f:
#         line_lower = data.lower()
#         if line_lower in seen:
#             print(data)
#         else:
#             seen.add(line_lower)
#     print seen