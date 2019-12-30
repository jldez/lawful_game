import people
import jobs
import goods_services
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import *
from matplotlib.widgets import *


COLORMAP = plt.cm.rainbow
COLORMAP_RANGE = (0.2,0.8)

# todo : fix annotation box going outside window 

class Run(object):
    def __init__(self):

        self.fig, self.axs = plt.subplots(figsize=(21,9), ncols=2, nrows=3)
        self.fig.canvas.set_window_title('Lawful Game')

        self.population = people.Population(200)
        self.time = [0]

        self.time_step = 1
        self.fig.text(0.03,0.96,'Time step')
        self.time_step_slider = Slider(plt.axes([0.03, 0.935, 0.05, 0.02]), None, 1, 100, valinit=1, valfmt='%3d', valstep=1, orientation='horizontal')
        self.time_step_slider.on_changed(self.change_time_step)

        self.resources_text = self.fig.text(0.03,0.9,'')

        self.fig.text(0.9,0.96,'Tax rate')
        self.tax_rate_slider = Slider(plt.axes([0.9, 0.935, 0.05, 0.02]), None, 0, 1, valinit=self.population.government.tax_rate, valfmt='%1.2f', valstep=0.01, orientation='horizontal')
        self.tax_rate_slider.on_changed(self.change_tax_rate)
        self.fig.text(0.9,0.9,'Social welfare')
        self.social_welfare_textbox = TextBox(plt.axes([0.9, 0.875, 0.05, 0.02]), None, initial='10000', color='.95', hovercolor='1')
        self.social_welfare_textbox.on_submit(self.change_social_welfare)
        self.fig.text(0.9,0.84,'Retirement age')
        self.retirement_age_slider = Slider(plt.axes([0.9, 0.815, 0.05, 0.02]), None, 0, 100, valinit=self.population.government.retirement_age, valfmt='%3d', valstep=1, orientation='horizontal')
        self.retirement_age_slider.on_changed(self.change_retirement_age)
        self.fig.text(0.9,0.78,'Healthcare')
        self.healthcare_slider = Slider(plt.axes([0.9, 0.755, 0.05, 0.02]), None, 0, 1, valinit=self.population.government.public_healthcare, valfmt='%1.2f', valstep=0.01, orientation='horizontal')
        self.healthcare_slider.on_changed(self.change_healthcare)
        
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
        self.jobs_colors = COLORMAP(np.linspace(COLORMAP_RANGE[0], COLORMAP_RANGE[1], len(jobs.JOBS)+3))
        self.jobs_names = list(jobs.JOBS.keys())+['Student','Unemployed','Retired']
        self.jobs_bars = self.jobs_ax.bar(self.jobs_names, self.job_stats, color=self.jobs_colors)
        for tick in self.jobs_ax.get_xticklabels():
            tick.set_rotation(45)
        plt.subplots_adjust(hspace=0.5)
        self.jobs_ax.get_yaxis().set_visible(False)
        self.jobs_ax.set(frame_on=False)
        self.jobs_ax.set_ylim(0, self.max_stats)

        x,y,w,h = self.jobs_ax.get_position().bounds
        self.job_options_button = Button(plt.axes([0.03,y,0.05,0.03]), 'Jobs options')
        self.job_options_button.on_clicked(self.open_job_options)

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
        self.display_history = True

        self.people_scatter_data = self.ax_people.scatter(self.population.positions[:,0],self.population.positions[:,1], cmap=COLORMAP, alpha=0.75)
        self.person_annotation = self.ax_people.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        self.person_annotation.set_visible(False)
        self.people_highlight_data = self.ax_people.scatter([],[], marker='o', s=50, color='r')

        self.update_plots()
        self.run()


    def run(self):
        self.updating = False
        self.freeze_hover = None
        self.fig.canvas.mpl_connect('key_press_event', self.update)
        self.fig.canvas.mpl_connect('motion_notify_event', self.hover)
        self.fig.canvas.mpl_connect('button_press_event', self.click)
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

        if event.key == 'h': #hide/show person's history in hover annotation
            self.display_history = not self.display_history

        if event.key in [' ']: #update
            for t in range(self.time_step):
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
        job_bar_heights[:-3] = [int(100*self.population.job_stats[name]/(np.floor(jobs.JOBS[name]['proportion']*len(self.population))+1e-9)) for name in jobs.JOBS]
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
        self.people_scatter_data.set_sizes(self.population.scores)
        self.people_scatter_data.set_color(self.population.colors)
        try: self.hover(self.last_hover)
        except: pass

        print(len(goods_services.AVAILABLE_GOODS['houses']))
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()


    @staticmethod
    def format_money(money):
        if np.abs(money) >= 10e9:
            return str(int(money/1e9))+'G'
        elif np.abs(money) >= 10e6:
            return str(int(money/1e6))+'M'
        elif np.abs(money) >= 10e3:
            return str(int(money/1e3))+'k'
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
        text = p.name + ' \n'
        text += p.status + ' \n'
        text += f'age: {p.age} \n'
        text += f'health: {int(p.health)} \n'
        text += f'happiness: {int(p.happiness)} \n'
        if p.job is not None:
            text += f'{p.job.name} \n'
            try: text += f'Aspiration: {p.job.job_aspiration} \n'
            except: pass
            text += f'salary: {int(p.job.salary)} \n'
        text += f'money: '+self.format_money(p.money)+' \n'
        text += f'education: {p.education} \n'
        text += f'experience: {p.experience} \n'
        text += f'belongings: {list(p.belongings.keys())} \n'
        if self.display_history:
            text += 'history: \n'
            for line in p.history:
                text += line+' \n'
        self.person_annotation.set_text(text[:-2])

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

        self.last_hover = event
        if self.freeze_hover is not None:
            event = self.freeze_hover

        while len(self.ax_people.patches) > 0:
            [patch.remove() for patch in self.ax_people.patches]

        vis = self.person_annotation.get_visible()

        if event.inaxes == self.ax_people:
            cont, ind = self.people_scatter_data.contains(event)
            if cont:
                self.update_annot(ind['ind'][0])
                self.person_annotation.set_visible(True)
            else:
                if vis:
                    self.person_annotation.set_visible(False)
                    self.freeze_hover = None # Disable freeze if selected person dies
        else:
            self.person_annotation.set_visible(False)

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

        highlight_positions = np.empty((0,2))
        highlight_scores = np.empty(0)
        if bar_name == 'Single males':
            highlight_positions = np.array([p.xy for p in self.population.single_males])
            highlight_scores = np.array([p.score for p in self.population.single_males])
        if bar_name == 'Single females':
            highlight_positions = np.array([p.xy for p in self.population.single_females])
            highlight_scores = np.array([p.score for p in self.population.single_females])
        if bar_name == 'Couples':
            highlight_positions = np.array([c.father.xy for c in self.population.couples]+[c.mother.xy for c in self.population.couples])
            highlight_scores = np.array([c.father.score for c in self.population.couples]+[c.mother.score for c in self.population.couples])
        if bar_name == 'Kids':
            highlight_positions = np.array([p.xy for p in self.population.kids])
            highlight_scores = np.array([p.score for p in self.population.kids])
        if bar_name == 'Unemployed':
            highlight_positions = np.array([p.xy for p in self.population.unemployed])
            highlight_scores = np.array([p.score for p in self.population.unemployed])
        if bar_name == 'Retired':
            highlight_positions = np.array([p.xy for p in self.population.retired])
            highlight_scores = np.array([p.score for p in self.population.retired])
        elif bar_name in self.jobs_names[:-2]:
            highlight_positions = np.array([p.xy for p in self.population if p.job is not None and p.job.name == bar_name])
            highlight_scores = np.array([p.score for p in self.population if p.job is not None and p.job.name == bar_name])

        self.people_highlight_data.set_offsets(highlight_positions)
        self.people_highlight_data.set_sizes(highlight_scores)
        if not self.updating:
            self.fig.canvas.draw_idle()

        

    def click(self, event):
        if event.inaxes in [self.stats_ax,self.jobs_ax,self.ax_people]:
            if event.button == 1:
                # Update hover highlights before freezing
                self.freeze_hover = self.last_hover
                self.hover(self.freeze_hover)
            elif event.button == 3:
                self.freeze_hover = None
                self.hover(self.last_hover)


    def change_time_step(self, time_step):
        self.time_step = int(time_step)
    def change_tax_rate(self, tax_rate):
        self.population.government.tax_rate = tax_rate
    def change_social_welfare(self, amount):
        self.population.government.social_welfare = int(amount)
    def change_retirement_age(self, retirement_age):
        self.population.government.retirement_age = retirement_age
    def change_healthcare(self, healthcare):
        self.population.government.public_healthcare = healthcare

    def open_job_options(self, event):
        self.job_options_window = plt.figure(figsize=(4,6))
        self.job_options_window.canvas.set_window_title('Jobs Options')
        self.textboxes = []

        N = len(jobs.JOBS)

        self.job_options_window.text(0.03,1-0.8/(N+2), 'Job')
        self.job_options_window.text(0.3,1-0.8/(N+2), 'base salary')
        self.job_options_window.text(0.55,1-0.8/(N+2), 'max salary')
        self.job_options_window.text(0.8,1-0.8/(N+2), 'max prop.')

        for i, name in enumerate(jobs.JOBS):

            self.job_options_window.text(0.03,1-(i+2)/(N+2), name)
            self.textboxes.append(TextBox(plt.axes([0.3, 1-(i+2)/(N+2)-0.005, 0.2, 0.03]), None, initial=str(int(jobs.JOBS[name]['base_salary'])), color='.95', hovercolor='1'))
            self.textboxes[-1].on_submit(changeJobOption(name, 'base_salary'))
            self.textboxes.append(TextBox(plt.axes([0.55, 1-(i+2)/(N+2)-0.005, 0.2, 0.03]), None, initial=str(int(jobs.JOBS[name]['max_salary'])), color='.95', hovercolor='1'))
            self.textboxes[-1].on_submit(changeJobOption(name, 'max_salary'))
            self.textboxes.append(TextBox(plt.axes([0.8, 1-(i+2)/(N+2)-0.005, 0.15, 0.03]), None, initial=str(jobs.JOBS[name]['proportion']), color='.95', hovercolor='1'))
            self.textboxes[-1].on_submit(changeJobOption(name, 'proportion'))

        plt.show()



class changeJobOption(object):
    def __init__(self, name, option):
        self.name = name
        self.option = option
    def __call__(self, event):
        if self.option == 'proportion':
            jobs.JOBS[self.name][self.option] = float(event)
        else:
            jobs.JOBS[self.name][self.option] = int(event)
            jobs.JOBS[self.name]['max_salary'] = max([jobs.JOBS[self.name]['base_salary'],jobs.JOBS[self.name]['max_salary']])

    


if __name__ == '__main__':
    run = Run()