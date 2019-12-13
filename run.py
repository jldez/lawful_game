import people
import matplotlib.pyplot as plt



class Run(object):
    def __init__(self):

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Population')
        self.pop = people.Population(50)
        self.time = [0]
        self.total = [len(self.pop)]
        self.aging = [self.pop.mean_age]
        self.line, = self.ax.plot(self.time,self.total)

        self.run()


    def run(self):
        self.tracking = self.total
        self.fig.canvas.mpl_connect('key_press_event', self.update)
        plt.show()


    def update(self, event):

        if event.key == 'r':
            self.pop = people.Population(50)
            self.time = [0]
            self.total = [len(self.pop)]
            self.aging = [self.pop.mean_age]

        if event.key in [' ']:
            self.pop.update()
            self.total.append(len(self.pop))
            self.time.append(len(self.total))
            self.aging.append(self.pop.mean_age)

        if event.key == 'p':
            self.tracking = self.total
            self.ax.set_title('Population')
        if event.key == 'a':
            self.tracking = self.aging
            self.ax.set_title('Mean age')
        
        self.line.set_data(self.time,self.tracking)
        self.ax.set_xlim(min(self.time),max(self.time))
        self.ax.set_ylim(min(self.tracking),max(self.tracking))
        plt.draw()

    


if __name__ == '__main__':
    run = Run()