import numpy as np
import matplotlib.pyplot as plt
x=np.array(np.linspace(-100,100,1000))
var = {'x':x,'sin':np.sin,'cos':np.cos,'sqrt':np.sqrt,'log':np.log,'abs':np.abs}
a="x**b"
if "x" not in a:
	a = "x-x+"+a
try:
	plt.plot(x, eval(a,var),"r-")
except OverflowError:
	print("Čísla jsou moc velká")
except NameError as e:
	print("Zadal jsi neznámou, kterou opravdu neznám")
	print(e)
plt.grid(True, which='both')
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.show()
