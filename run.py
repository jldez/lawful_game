import people
import numpy as np
import matplotlib.pyplot as plt
import tqdm



class Run(object):
    def __init__(self):

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Lawful Game')

        self.pop = people.Population(50)
        self.time = [0]
        self.total = [len(self.pop)]
        self.line, = self.ax.plot(self.time,self.total)

        self.run()


    def run(self):
        self.fig.canvas.mpl_connect('key_press_event', self.update)
        plt.show()


    def update(self, event):

        if event.key == 'r':
            self.pop = people.Population(50)
            self.time = [0]
            self.total = [len(self.pop)]

        if event.key in [' ']:
            self.pop.update()
            self.total.append(len(self.pop))
            self.time.append(len(self.total))

        self.line.set_data(self.time,self.total)
        self.ax.set_xlim(min(self.time),max(self.time))
        self.ax.set_ylim(min(self.total),max(self.total))
        plt.draw()

    


if __name__ == '__main__':
    run = Run()