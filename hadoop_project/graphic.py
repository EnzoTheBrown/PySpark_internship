import matplotlib.pyplot as plt
import numpy as np

f = open("info", "r")
lignes  = f.readlines()
c1 = []
c2 = []
c3 = []
for ligne in lignes:
	list = ligne.split(" ",2)
	for l in list:
		c1.append(l[0])
		c2.append(l[1])
		c3.append(l[2])

x = []
x = array(c1)
y = array(c2)
z = array(c3)
plt.plot(x, y, label="hive")
plt.plot(x, z, label="impala")
plt.title("Execution's time of a query on a data set with hive and impala")
plt.xlabel("time/s")
plt.ylabel("data /Mo")
plt.legend()
plt.show()

f.close()