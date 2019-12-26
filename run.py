import people
import jobs
import matplotlib.pyplot as plt
from matplotlib.patches import *
import numpy as np

COLORMAP = plt.cm.rainbow
COLORMAP_RANGE = (0.2,0.8)



class Run(object):
    def __init__(self):

        self.fig, self.axs = plt.subplots(figsize=(21,9), ncols=2, nrows=3)

        self.population = people.Population(200)
        self.time = [0]

        self.resources_text = self.fig.text(0.03,0.93,'')
        
        self.stats_ax = self.axs[0,0]
        self.stats_colors = COLORMAP(np.linspace(COLORMAP_RANGE[0], COLORMAP_RANGE[1], len(self.population.stats)))
        self.stats_bars = self.stats_ax.bar(self.population.stats_names, self.stats_values, color=self.stats_colors)
        for tick in self.stats_ax.get_xticklabels():
            tick.set_rotation(45)
        self.stats_ax.get_yaxis().set_visible(False)
        self.stats_ax.set(frame_on=False)
        self.max_stats = 100
        self.stats_ax.set_ylim(0, self.max_stats)

        self.jobs_ax = self.axs[1,0]
        self.jobs_colors = COLORMAP(np.linspace(COLORMAP_RANGE[0], COLORMAP_RANGE[1], len(jobs.JOBS)+2))
        self.jobs_names = list(jobs.JOBS.keys())+['student','unemployed']
        self.jobs_bars = self.jobs_ax.bar(self.jobs_names, self.job_stats, color=self.jobs_colors)
        for tick in self.jobs_ax.get_xticklabels():
            tick.set_rotation(45)
        plt.subplots_adjust(hspace=0.5)
        self.jobs_ax.get_yaxis().set_visible(False)
        self.jobs_ax.set(frame_on=False)
        self.jobs_ax.set_ylim(0, self.max_stats)

        self.track_ax = self.axs[2,0]
        self.track_stats = {name:[self.population.stats[name]] for name in self.population.stats_names}
        self.tracking_name = list(self.track_stats.keys())[0]
        self.track_ax.set_ylabel(self.tracking_name)
        self.track_line, = self.track_ax.plot(self.time, self.track_stats[self.tracking_name], color=self.stats_colors[0])

        gs = self.axs[0,1].get_gridspec()
        for ax in self.axs[:,-1]:
            ax.remove()
        self.ax_people = self.fig.add_subplot(gs[:,-1], frame_on=False)
        self.ax_people.get_xaxis().set_visible(False)
        self.ax_people.get_yaxis().set_visible(False)

        self.people_scatter_data = self.ax_people.scatter(self.population.positions[:,0],self.population.positions[:,1])
        self.person_annotation = self.ax_people.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        self.person_annotation.set_visible(False)
        self.people_highlight_data = self.ax_people.scatter([],[], marker='o', s=50, color='r')

        self.update_plots()
        self.run()


    def run(self):
        self.updating = False
        self.fig.canvas.mpl_connect('key_press_event', self.update)
        self.fig.canvas.mpl_connect('motion_notify_event', self.hover)
        plt.show()

    
    @property
    def stats_values(self):
        return [self.population.stats[name] for name in self.population.stats]
    @property
    def job_stats(self):
        return [self.population.job_stats[name] for name in self.population.job_stats]

    def update(self, event):
        if self.updating:
            return 0

        self.updating = True

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
        self.updating = False


    def update_plots(self):

        self.resources_text.set_text('Money:' + self.format_money(self.population.government.money) + f' | Food:{self.population.food}')

        while len(self.stats_ax.texts) > 0:
            [txt.remove() for txt in self.stats_ax.texts]
        while len(self.jobs_ax.texts) > 0:
            [txt.remove() for txt in self.jobs_ax.texts]

        i=0
        for bar, h in zip(self.stats_bars, self.stats_values):
            bar.set_height(self.rescale_bar_height(h))
            self.stats_ax.text(bar.get_x() + bar.get_width()/2, self.rescale_bar_height(h), f'{int(h)}', ha='center', va='bottom')
            i+=1

        i=0
        job_bar_heights = self.job_stats
        job_bar_heights[:-2] = [int(100*self.population.job_stats[name]/(np.floor(jobs.JOBS[name]['proportion']*len(self.population))+1e-9)) for name in jobs.JOBS]
        for bar, n, h in zip(self.jobs_bars, self.job_stats, job_bar_heights):
            bar.set_height(self.rescale_bar_height(h))
            self.jobs_ax.text(bar.get_x() + bar.get_width()/2, self.rescale_bar_height(h), f'{int(n)}', ha='center', va='bottom')
            i+=1

        max_length = 100
        data = self.track_stats[self.tracking_name]
        self.track_line.set_data(self.time[-max_length:],data[-max_length:])
        self.track_ax.set_ylabel(self.tracking_name)
        if max(data[-max_length:]) > min(data[-max_length:]):
            self.track_ax.set_xlim(min(self.time[-max_length:]),max(self.time[-max_length:]))
            self.track_ax.set_ylim(min(data[-max_length:]),max(data[-max_length:]))

        self.people_scatter_data.set_offsets(self.population.positions)
        try: self.hover(self.last_hover)
        except: pass

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    @staticmethod
    def format_money(money):
        if np.abs(money) >= 1e9:
            return str(int(money/1e9))+'G'
        elif np.abs(money) >= 1e6:
            return str(int(money/1e6))+'M'
        else:
            return str(int(money))


    def rescale_bar_height(self, h):
        transition_frac = 0.75
        if h <= self.max_stats*transition_frac:
            return h
        else:
            h = self.max_stats*transition_frac + np.log(h-self.max_stats*transition_frac)
            return h if h <= self.max_stats else self.max_stats


    def update_annot(self, ind):
        self.person_annotation.xy = self.people_scatter_data.get_offsets()[ind]
        p = self.population.persons[ind]
        text = p.status + ' \n'
        text += f'age: {p.age} \n'
        text = text + f'{p.job.name} \n' if p.job is not None else text+'unemployed \n'
        text += f'money: {int(p.money)}'
        self.person_annotation.set_text(text)

        connections = []
        for parent in [p.father, p.mother]:
            if parent is not None:
                connections.append(ConnectionPatch(p.xy, parent.xy, 'data', color='b'))
        if p.couple is not None:
            connections.append(ConnectionPatch(p.couple.father.xy, p.couple.mother.xy, 'data', color='r'))
        if len(p.kids) > 0:
            connections += [ConnectionPatch(p.xy, kid.xy, 'data', color='y') for kid in p.kids]
        if len(connections) > 0:
            [self.ax_people.add_patch(connection) for connection in connections]
        

    def hover(self, event):

        while len(self.ax_people.patches) > 0:
            [patch.remove() for patch in self.ax_people.patches]

        vis = self.person_annotation.get_visible()

        if event.inaxes == self.ax_people:
            cont, ind = self.people_scatter_data.contains(event)
            if cont:
                self.update_annot(ind['ind'][0])
                self.person_annotation.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.person_annotation.set_visible(False)
                    self.fig.canvas.draw_idle()

        bar_name = ''
        if event.inaxes == self.stats_ax:
            for i, bar in enumerate(self.stats_bars):
                cont,_ = bar.contains(event)
                if cont:
                    bar_name = self.population.stats_names[i]
        elif event.inaxes == self.jobs_ax:
            for i, bar in enumerate(self.jobs_bars):
                cont,_ = bar.contains(event)
                if cont:
                    bar_name = self.jobs_names[i]

        highlight_positions = np.empty((1,2))
        if bar_name == 'Single males':
            highlight_positions = np.array([p.xy for p in self.population.single_males])
        if bar_name == 'Single females':
            highlight_positions = np.array([p.xy for p in self.population.single_females])
        if bar_name == 'Couples':
            highlight_positions = np.array([c.father.xy for c in self.population.couples]+[c.mother.xy for c in self.population.couples])
        if bar_name == 'Kids':
            highlight_positions = np.array([p.xy for p in self.population.kids])
        if bar_name == 'unemployed':
            highlight_positions = np.array([p.xy for p in self.population.unemployed])
        elif bar_name in self.jobs_names:
            highlight_positions = np.array([p.xy for p in self.population if p.job is not None and p.job.name == bar_name])

        if event.inaxes in [self.stats_ax, self.jobs_ax]:
            self.people_highlight_data.set_offsets(highlight_positions)
            self.fig.canvas.draw_idle()

        self.last_hover = event


if __name__ == '__main__':
    run = Run()