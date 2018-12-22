import numpy as np
import matplotlib.pyplot as plt

def graph(formula, x_range):
    x = np.array(x_range)
    y = eval(formula)
    plt.plot(x, y, 'r--')   # `r--` for dashed red line
    plt.show()

graph('((x-3) * (x-2))',np.linspace(-3,3,100))  # <----