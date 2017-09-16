import os
import sys
import string


#定位文件
#sys.argv[0] 返回文件名
path = os.path.dirname(os.path.abspath(sys.argv[0])) + '\\data.txt';
file = open(path, mode='r')


# The max score of math
maxMath = -1
stuName = ''
stuId = ''
ls = file.readlines() #read(), readline(), readlines()
ls.pop(0) #删除第一行
for l in ls:
    word = l.split('\t')
    if int(word[3]) > maxMath:
        maxMath = int(word[3])
        stuName = word[0]
        stuId = word[1]

print("The max score of math is %d, name is %s and id is %s" % (maxMath, stuName, stuId))
file.close()

#string to number url: http://blog.csdn.net/u010412719/article/details/46820841