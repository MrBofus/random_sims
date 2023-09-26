import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


class plot():
    def __init__(self, plot_function, initial_parameters, slider_parameters, *argv):

        self.runfunct = plot_function

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.15, bottom=0.25)

        self.response = self.runfunct(initial_parameters)
        self.plots = []

        if not len(argv) == 0:
            for i in range(1, len(self.response)):
                _, = plt.plot(self.response[0], self.response[i], label = argv[0]['LABELS'][i-1], color = argv[0]['COLORS'][i-1])
                self.plots.append( _ )
            ymin = argv[0]['YMIN']
            ymax = argv[0]['YMAX']
            if not ymin == ymax:
                self.ax.set_ylim([1.1*ymin, 1.1*ymax])
            plt.legend()
        
        else:
            for i in range(1, len(self.response)):
                _, = plt.plot(self.response[0], self.response[i])
                self.plots.append( _ )
        
        self.ax.margins(x=0)
        plt.grid()

        axcolor = 'lightgoldenrodyellow'
        self.axws = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        self.sws = Slider(self.axws, slider_parameters['SLIDER_NAME'], 
                                     slider_parameters['SLIDER_MIN'],
                                     slider_parameters['SLIDER_MAX'],
                                     valinit=slider_parameters['SLIDER_INIT'],
                                     valstep=slider_parameters['SLIDER_STEP'])

        def update(val):

            slider_val = self.sws.val
            if argv[1]:
                slider_val = argv[1](slider_val)
            self.sws.valtext.set_text(slider_val)

            ranges = self.runfunct( slider_val )

            for i in range(1, len(ranges)):
                self.plots[i-1].set_xdata(ranges[0])
                self.plots[i-1].set_ydata(ranges[i])

            '''
            ymin = min(ranges[1])
            ymax = max(ranges[1])
            for i in range(2, len(ranges)):
                yminl = min(ranges[i])
                ymaxl = max(ranges[i])

                if ymaxl > ymax:
                    ymax = ymaxl
                
                if yminl < ymin:
                    ymin = yminl
            '''

            self.ax.set_xlim([int(1.1*min(ranges[0])), int(1.1*max(ranges[0]))])
            if not len(argv) == 0:
                ymin = argv[0]['YMIN']
                ymax = argv[0]['YMAX']
                if not ymin == ymax:
                    self.ax.set_ylim([1.1*ymin, 1.1*ymax])

            self.fig.canvas.draw_idle()

        self.sws.on_changed(update)
        plt.show()


def update_old(plots, swsaxes, axes, figure, runfunct):

        slider_val = swsaxes.val
        slider_val = slider_val
        swsaxes.valtext.set_text(int(slider_val))

        ranges = runfunct( int(slider_val) )

        for i in range(1, len(ranges)):
            plots[i-1].set_xdata(ranges[0])
            plots[i-1].set_ydata(ranges[i])

        ymin = min(ranges[1])
        ymax = max(ranges[1])
        for i in range(2, len(ranges)-1):
            yminl = min(ranges[i])
            ymaxl = max(ranges[i])

            if ymaxl > ymax:
                ymax = ymaxl
            
            if yminl < ymin:
                ymin = yminl

        axes.set_xlim([int(1.1*min(ranges[0])), int(1.1*max(ranges[0]))])
        axes.set_ylim([1.1*ymin, 1.1*ymax])
        figure.canvas.draw_idle()