import sys
import math
import numpy as np
import matplotlib.pyplot as plt
array_a=[]
array_b=[]
a = int(input("A?: "))
b = int(input("B?: "))
c = int(input("C?: "))
#a,b,c=1,7,10
def dis(a,b,c):
	d = b**2 - 4*a*c
	if d < 0:
		print("Diskriminant je menší než nula, nelze řešit!")
		sys.exit()
	return d
def solve(a,b,c):
	d = dis(a,b,c)
	if d==0:
		xst=(-b/2*a)
		print(f"X je {xst}")
		return None
	else:
		xst = (-b+math.sqrt(d))/2*a
		xnd = (-b-math.sqrt(d))/2*a
		x = np.linspace(int(xst), int(xnd), 1000)
		y = a*x**2+b*x+c
		#print(y)
		fig, ax = plt.subplots()
		ax.plot(x, y)
		plt.savefig('plottwist.png',bbox_inches='tight')
print()
solve(a,b,c)
input()
