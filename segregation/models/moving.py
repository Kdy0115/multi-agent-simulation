import numpy as np
import matplotlib.pyplot as plt


class MovingSpanModel():
    def __init__(self):
        self.x_demo = np.linspace(0, 10, 257)
        self.k = 1
        self.x0 = 1
        self.a = 1
        self.y_demo = self.logistic(self.x_demo, self.a, self.k, self.x0)
    
    def logistic(self, x, a=1, k=1, x0=1):
        y = k / (1 + np.exp(-a * k * (x - x0)))
        return y

    def show_graph(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.grid(linestyle = "--")
        ax.set_title("Logistic Function", fontsize = 16)
        ax.set_xlim(0, 10)
        ax.set_xlabel("x", fontsize = 16)
        ax.set_ylabel("y", fontsize = 16)
        ax.plot(self.x_demo, self.y_demo)
        plt.show()
        