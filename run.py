import people
import matplotlib.pyplot as plt
import numpy as np



class Run(object):
    def __init__(self):

        self.fig = plt.figure('Lawful Game')

        self.population = people.Population(50)

        self.stats_ax = self.fig.add_subplot(211)
        self.stats_names = ['Population','Mean age']
        self.stats = [len(self.population), self.population.mean_age]
        self.stats_bars = self.stats_ax.bar(self.stats_names, self.stats)
        self.stats_ax.get_yaxis().set_visible(False)
        self.max_stats = 100
        self.stats_ax.set_ylim(0,self.max_stats)

        self.track_ax = self.fig.add_subplot(212)
        self.time = [0]
        self.track_population = [len(self.population)]
        self.track_mean_age = [self.population.mean_age]
        self.track_ax.set_ylabel('Population')
        self.tracking = self.track_population
        self.track_line, = self.track_ax.plot(self.time,self.track_population)

        self.update_plots()
        self.run()


    def run(self):
        self.fig.canvas.mpl_connect('key_press_event', self.update)
        plt.show()


    def update(self, event):

        if event.key == 'r': #restart
            plt.clf()
            self.__init__()

        if event.key in [' ']: #update
            self.population.update()
            self.track_population.append(len(self.population))
            self.time.append(len(self.track_population))
            self.track_mean_age.append(self.population.mean_age)

        if event.key == 'p': #population graph
            self.tracking = self.track_population
            self.track_ax.set_ylabel('Population')
        if event.key == 'a': #aging graph
            self.tracking = self.track_mean_age
            self.track_ax.set_ylabel('Mean age')

        self.update_plots()


    def update_plots(self):

        while len(self.stats_ax.texts) > 0:
            [txt.remove() for txt in self.stats_ax.texts]

        self.stats = [self.track_population[-1], self.track_mean_age[-1]]
        i=0
        for bar, h in zip(self.stats_bars, self.stats):
            bar.set_height(self.rescale_bar_height(h))
            self.stats_ax.text(i-0.17,self.rescale_bar_height(h),'{:10d}'.format(int(h)))
            i+=1

        max_length = 100
        self.track_line.set_data(self.time[-max_length:],self.tracking[-max_length:])
        if max(self.tracking[-max_length:]) > min(self.tracking[-max_length:]):
            self.track_ax.set_xlim(min(self.time[-max_length:]),max(self.time[-max_length:]))
            self.track_ax.set_ylim(min(self.tracking[-max_length:]),max(self.tracking[-max_length:]))
        plt.draw()


    def rescale_bar_height(self, h):
        transition_frac = 0.75
        if h <= self.max_stats*transition_frac:
            return h
        else:
            h = self.max_stats*transition_frac + np.log(h-self.max_stats*transition_frac)
            return h if h <= self.max_stats else self.max_stats
            
    


if __name__ == '__main__':
    run = Run()