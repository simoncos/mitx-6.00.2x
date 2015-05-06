# -*- coding: utf-8 -*-

import pylab
import numpy as np

def loadFileTest(): # 从文本中读取最高温度和最低温度并分别输出为list
    inFile = open("julyTemps.txt",'r',0)
    high = []
    low = []
    fields = []
    for line in inFile.readline(): # 这里的line便是每一行中的每一个字符了
        fields += str.split(line)
    return fields

def loadFile(): # 从文本中读取最高温度和最低温度并分别输出为list
    inFile = open("julyTemps.txt")
    high = []
    low = []
    for line in inFile:
        fields = line.split() # 等同于：fields = str.split(line)
        if len(fields) != 3 or 'Boston' == fields[0] or 'Day' == fields[0]: # 排除文本中的多余行
            continue # 继续遍历下一行
        else:
            high.append(int(fields[1])) # 类型转换为int后append到list
            low.append(int(fields[2]))
    return (low, high)

def producePlot(lowTemps, highTemps): # 用pylab图形输出每天的温差
    diffTemps = list(np.array(highTemps) - np.array(lowTemps)) # list之间无法相加减，所以使用了numpy库的array方法
    pylab.plot(range(1,32), diffTemps)
    pylab.title('Day by Day Ranges in Temperature in Boston in July 2012')
    pylab.xlabel('Days')
    pylab.ylabel('Temperature Ranges')
    pylab.show()
    
        
(low, high) = loadFile() #主函数入口   
producePlot(low, high)

print (np.array(low) - np.array(high)) # 测试numpy库的array方法的输出形式