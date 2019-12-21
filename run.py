import people
import jobs
import matplotlib.pyplot as plt
import numpy as np

COLORMAP = plt.cm.rainbow
COLORMAP_RANGE = (0.2,0.8)


class Run(object):
    def __init__(self):

        self.fig = plt.figure('Lawful Game', figsize=(12,8))

        self.population = people.Population(100)
        self.time = [0]
        
        self.stats_ax = self.fig.add_subplot(311)
        self.stats_colors = COLORMAP(np.linspace(COLORMAP_RANGE[0], COLORMAP_RANGE[1], len(self.population.stats)))
        self.stats_bars = self.stats_ax.bar(self.population.stats_names, self.stats_values, color=self.stats_colors)
        self.stats_ax.get_yaxis().set_visible(False)
        self.stats_ax.set(frame_on=False)
        self.max_stats = 100
        self.stats_ax.set_ylim(0, self.max_stats)

        self.jobs_ax = self.fig.add_subplot(312)
        self.jobs_colors = COLORMAP(np.linspace(COLORMAP_RANGE[0], COLORMAP_RANGE[1], len(jobs.JOBS)+2))
        self.jobs_bars = self.jobs_ax.bar(list(jobs.JOBS.keys())+['student','unemployed'], self.job_stats, color=self.jobs_colors)
        self.jobs_ax.get_yaxis().set_visible(False)
        self.jobs_ax.set(frame_on=False)
        self.jobs_ax.set_ylim(0, self.max_stats)

        self.track_ax = self.fig.add_subplot(313)
        self.track_stats = {name:[self.population.stats[name]] for name in self.population.stats_names}
        self.tracking_name = list(self.track_stats.keys())[0]
        self.track_ax.set_ylabel(self.tracking_name)
        self.track_line, = self.track_ax.plot(self.time, self.track_stats[self.tracking_name], color=self.stats_colors[0])

        self.update_plots()
        self.run()


    def run(self):
        self.fig.canvas.mpl_connect('key_press_event', self.update)
        plt.show()

    
    @property
    def stats_values(self):
        return [self.population.stats[name] for name in self.population.stats]
    @property
    def job_stats(self):
        return [self.population.job_stats[name] for name in self.population.job_stats]

    def update(self, event):

        if event.key == 'r': #restart
            plt.clf()
            self.__init__()

        if event.key in [' ']: #update
            self.population.update()
            self.time.append(len(self.time))
            for name in self.population.stats_names:
                self.track_stats[name].append(self.population.stats[name])

        if event.key in ['right','left']: #Tracking
            track_index = list(self.track_stats.keys()).index(self.tracking_name)
            track_index = track_index+1 if event.key == 'right' else track_index-1
            track_index = np.clip(track_index, 0, len(self.track_stats)-1)
            self.tracking_name = list(self.track_stats.keys())[track_index]
            self.track_line.set_color(self.stats_colors[track_index])

        self.update_plots()


    def update_plots(self):

        while len(self.stats_ax.texts) > 0:
            [txt.remove() for txt in self.stats_ax.texts]
        while len(self.jobs_ax.texts) > 0:
            [txt.remove() for txt in self.jobs_ax.texts]

        i=0
        for bar, h in zip(self.stats_bars, self.stats_values):
            bar.set_height(self.rescale_bar_height(h))
            self.stats_ax.text(i-0.4,self.rescale_bar_height(h),'{:10d}'.format(int(h)))
            i+=1

        i=0
        for bar, h in zip(self.jobs_bars, self.job_stats):
            bar.set_height(self.rescale_bar_height(h))
            self.jobs_ax.text(i-0.4,self.rescale_bar_height(h),'{:10d}'.format(int(h)))
            i+=1

        max_length = 100
        data = self.track_stats[self.tracking_name]
        self.track_line.set_data(self.time[-max_length:],data[-max_length:])
        self.track_ax.set_ylabel(self.tracking_name)
        if max(data[-max_length:]) > min(data[-max_length:]):
            self.track_ax.set_xlim(min(self.time[-max_length:]),max(self.time[-max_length:]))
            self.track_ax.set_ylim(min(data[-max_length:]),max(data[-max_length:]))
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