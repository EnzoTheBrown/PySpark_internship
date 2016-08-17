"""myContext.py""" 

import pickle
import sys 
import re 
import time
import calendar
import datetime

#from operator import min
from datetime import timedelta
from pyspark import SparkContext 

def max(a, b):
	if a > b:
		return a
	return b 

def min(a, b):
	if a < b:
		return a
	return b

def max_min(max_min, eval):
	(max, min) = max_min
	if max < eval:
		return (eval, min)
	if min > eval:
		return (max, eval)
	return (max, min)	

def convert_H_to_S(H):
	L = re.split(':', H)
	res = int(L[0])*3600 + int(L[1])*60 + int(L[2])
	return(res)

def convert_S_to_H(S):
    H = str(int(S/(3600)))
    S %= 3600
    if int(H) < 0:
        return None
    if int(H) < 10:
        H = ('0'+H)
    M = str(int(S/60))
    if int(M) < 10:
        M = ('0'+M)
    S %= 60
    if S > 10:
        S = str(S)
    else:
        S = ('0%i' %S)
    return H+':'+M+':'+S

def get_hour(add, line, list):
	hour = re.findall(r'[0-2][0-9]:[0-6][0-9]:[0-6][0-9]', line)[0]
	list.append(hour)
	return list

def manhattan(xa, ya, xb, yb):
    return abs(xa - xb) + abs(ya - yb)

def get_day_from_date(date):
	my_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	return calendar.day_name[my_date.weekday()]	

def to_add(list1, list2):
	#for each address in list2 we are looking if they are in list1 if not we add them
        for address in list2:
        	if address not in list1:
                	list1.append(address)
        return list1

def not_match(list, line):
	if len(re.split('\s+', line)) < 5:
		list.append(line)
	return list 

class myContext():
	def __init__(self, context, name, file):
		self.sc = SparkContext(context, name)
		self.rdd = self.sc.textFile(file)

	def to_add(self, list1, list2):
		#for each address in list2 we are looking if they are in list1 if not we add them
		for address in list2:
			if address not in list1:
				list1.append(address)
		return list1

	def address_lister(self):
		''' get one of each address mac of the file '''
        	myList = []
		res = self.rdd\
			.map(lambda str: to_add(myList, re.findall(r'((?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})', str)))		
		return res.collect().pop()

	def get_hour_activity(self, address):
		''' for each address mac we'll see when they are mostly connect'''
		myList = []
		res = self.rdd\
			.filter(lambda str: address in str)\
			.map(lambda str: get_hour(address, str, myList))
		return res.collect().pop()

	def get_max_hour_activity(self, address):
		''' get the max hour of activity for an address '''
		res = self.rdd\
			.filter(lambda str: address in str)\
			.map(lambda str: re.findall(r'[0-2][0-9]:[0-6][0-9]:[0-6][0-9]', str)[0])\
			.map(lambda str: convert_H_to_S(str))\
			.reduce(max)
		return res

	def get_min_hour_activity(self, address):
		res = self.rdd\
                        .filter(lambda str: address in str)\
                        .map(lambda str: re.findall(r'[0-2][0-9]:[0-6][0-9]:[0-6][0-9]', str)[0])\
                        .map(lambda str: convert_H_to_S(str))\
                        .reduce(min)
                return res	

	def get_day_activity(self, address):
		''' return a list of day of activity '''
		res = self.rdd\
			.filter(lambda str: address in str)\
			.map(lambda str: re.findall(r'(\d{4}(?:-(?:\d){2}){2})', str)[0])\
			.map(lambda date: get_day_from_date(date))\
			.distinct()\
			.count()
		return res			

	def parallelize_list(self, list):
		return self.sc.parallelize(list)

	def save_list(self, list, file):
		mac_file = open(file, 'w+')
		for line in list:
			mac_file.write(line + ' \n')
		mac_file.close()
		'''Save the result into a file'''

	def usual_suspect(self, address):
		min = 86400
		max = 0
		res = self.rdd\
		.filter(lambda line: address in line)\
		.map(lambda line: re.split(r'\s+', line))\
		.map(lambda line: [line[0], convert_H_to_S(line[1])])\
		.reduceByKey(min)\
		.take(10)
#		.reduceByKey(min)\
#		.map(lambda line: [get_day_from_date(line[0]), line[1]])\
#		.filter(lambda line: 'Friday' in line[0])\
#		.map(lambda line: line[1])\
#		.count()

		return res

if __name__ == "__main__":
	argList = sys.argv[1:]
	CC = myContext('spark://master:7077', 'list address mac', 'hdfs://master:54310/user/hduser1/wifi')
	if '-ls' in argList:
		L = CC.address_lister()
		CC.save_list(L, 'mac_address_wifi')
	if '-act' in argList:
		res = CC.get_hour_activity('00:19:07:8d:ed:53')
		avg = CC.parallelize_list(res).map(lambda line: convert_H_to_S(line)).mean()
		print(convert_S_to_H(avg))
	if '-range' in argList:
		L = re.split('\n', open(argList[argList.index('-range') + 1], 'r').read())
		res = open('mac_address_time', 'w+')
		for add in L:
			print('______ NEW ADDRESS _____')
			print('')
			print(add)
			print('')
			print('________________________')
			max = convert_S_to_H(CC.get_max_hour_activity(add))
			min = convert_S_to_H(CC.get_min_hour_activity(add))

			print('_____ RESULT _____')
			print('')
			print(max)
			print(min)
			print('')
			print('__________________')
			res.write(add + ':\n    max: ' + max + '\n    min: ' + min + '\n')
		res.close()
	if '-day' in argList:
		L = re.split(r'\n', open('mac_address', 'r').read())
		file = open('mac_address_day', 'w+')
		for add in L:
			days = CC.get_day_activity(add)
			file.write(add+': ' + str(days)+'\n')
		file.close()
	if '-suspect' in argList:
		print(CC.usual_suspect('00:19:07:8d:ed:53'))

#	for address in L:
#		print(' ______ NEW ADDRESS ______')
#		print('')
#		print(address)
#		print('')
#		print('__________________________')
#		paranormal_activity.append(CC.get_hour_activity(address))
#	print('________ FINAL RESULT _______')
#	print('')
#	print(len(paranormal_activity))
#        print(convert_S_to_H(avg))
#	print('')
#	print('____________________________')
#	print(L)

#	CC.save_list(L, 'mac_address')


#	CC.first_line()
#	CC.not_match()
