import pulp
import matplotlib.pyplot as plt
import numpy as np

def fp(x,p):
    return

def plot_fp(p):
    "Plots the function fp with parameter p in the interval (a,b)"
    # here we get the min and max of the data
    a = np.min(xdata)
    b = np.max(xdata)
    # generate a set of x points in the interval min(xdata), max(ydata)
    xplot = np.linspace(a,b,100)
    # evaluate the generated points in the function with the parameter p
    yplot = fp(xplot,p)
    # plot the data
    plt.plot(xdata,ydata,'ro')
    # plot the function
    plt.plot(xplot,yplot,'b')

def error_cuadratico(p):
    error = 0
    for i in range(len(xdata)):
        plot_fp()
        error = error + (fp(xdata[i], p) - ydata[i]) ** 2
    return error


xdata = range(0, 14)
ydata = [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000]
