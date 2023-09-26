import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

def real_gyro_measurement(t):
    return 10*np.sin(0.5*t)

def pull_gyro_measurement(w):
    return w + np.random.normal(0, 3)

def low_pass_filter(p_measurements, window_size):

    # initialize average to zero
    avg_of_window = 0

    # iterate through the last 'window_size' number of
    # elements in the 'p_measurements' array
    for i in range(1, window_size+1):

        # sum the most recent 'window_size' measurements
        avg_of_window += p_measurements[-i]
    
    # devide the sum by the number of elements averaged,
    # giving the average in the window
    avg_of_window /= window_size

    # return average measurement
    return avg_of_window

def runfunct(size_of_window):
    ##````````````````````````````````````````````````````````````````````````````````````````````````##
    # initialize parameters

    # initialize the arrays for graphing purposes
    angular_rates_real = []         # array for storing the real angular rates ("true data")
    angular_rates_measured = []     # array for storing the measured angular rates ("error-filled data")
    angular_rates_filtered = []     # array for storing the filtered angular rates
    times = []                      # array for storing time values at each incriment

    # initialize simulation parameters
    t = 0         # initial time at zero
    dt = 0.01     # timestep of 0.01 seconds
    t_max = 10    # number of seconds to simulate


    ##````````````````````````````````````````````````````````````````````````````````````````````````##
    # simulation loop

    while t < t_max:

        # determine the true angular rate of the spacecraft
        w_real = real_gyro_measurement(t)

        # have rate gyro make an angular rate measurement
        w_measured = pull_gyro_measurement(w_real)

        # append the real and measured values to their respective arrays
        angular_rates_real.append(w_real)
        angular_rates_measured.append(w_measured)


        # if the proper number of datapoints has been collected to initialize the filter,
        # enter this loop
        if len(angular_rates_measured) > size_of_window:

            # determine the filtered angular rate using our filter,
            # passing it the array of measured angular rates and the window size variable
            w_filtered = low_pass_filter(angular_rates_measured, size_of_window)

            # append filtered measurement to its list
            angular_rates_filtered.append(w_filtered)
        
        # otherwise, have store a '0' for filtered angular rate, as the 
        # filter is un-initialized at this stage
        else:
            angular_rates_filtered.append(0)


        # append the time to its array for graphing purposes
        times.append(t)

        # increment the time by 'dt'
        t += dt
    
    return times, angular_rates_real, angular_rates_measured, angular_rates_filtered





fig, ax = plt.subplots()
plt.subplots_adjust(left=0.15, bottom=0.25)

t, s1, s2, s3 = runfunct(20)

l2, = plt.plot(t, s2, color = 'blue', label='measured angular rate', alpha=0.8, lw=2)
l1, = plt.plot(t, s1, color = 'orange', label='true angular rate', lw=2)
l3, = plt.plot(t, s3, color = 'red', label='filtered angular rate', lw=2)
ax.margins(x=0)

plt.grid()
plt.legend()

axcolor = 'lightgoldenrodyellow'
axws = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

sws = Slider(axws, 'window size', 1, 2.491361694, valinit=1.477121255, valstep=0.00001)
sws.valtext.set_text(20)


def update(val):
    freq = sws.val
    freq = 10**freq - 9
    sws.valtext.set_text(int(freq))

    x, y1, y2, y3 = runfunct( int(freq) )

    l1.set_xdata(x)
    l1.set_ydata(y1)

    l2.set_xdata(x)
    l2.set_ydata(y2)

    l3.set_xdata(x)
    l3.set_ydata(y3)

    ax.set_xlim([int(1.1*min(x)), int(1.1*max(x))])
    ax.set_ylim([-15, 15])
    fig.canvas.draw_idle()


sws.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    sws.reset()
button.on_clicked(reset)

plt.show()