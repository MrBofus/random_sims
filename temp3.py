import interactive_plots as iplt
import numpy as np

'''
def plot_a_sin(w):
    
    times = []
    amplitude1 = []
    amplitude2 = []

    t = 0
    dt = 0.001
    t_final = 10
    while t < t_final:

        times.append(t)
        amplitude1.append(3*np.sin(w*t))
        amplitude2.append(5*np.cos(w*t))

        t += dt
    
    return times, amplitude1, amplitude2


initial_value = 0.3

sliderparams = {'SLIDER_NAME': 'frequency', 'SLIDER_MIN': 0, 'SLIDER_MAX': 1, 'SLIDER_INIT': initial_value, 'SLIDER_STEP': 0.01}
plotparams = {'LABELS': ['sine', 'cosine'], 
              'COLORS': ['blue', 'red'],
              'YMIN':0, 'YMAX':0}
plots = iplt.plot(plot_a_sin, initial_value, sliderparams, plotparams)
'''

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
    
    return times, angular_rates_measured, angular_rates_real, angular_rates_filtered

def sliderfunct(val):
    return int(10**val - 9)
    

initial_value = np.log10(20)

sliderparams = {'SLIDER_NAME': 'window size', 'SLIDER_MIN': np.log10(10), 'SLIDER_MAX': np.log10(300), 'SLIDER_INIT': initial_value, 'SLIDER_STEP': 0.00001}
plotparams = {'LABELS': ['measured angular rate', 'real angular rate', 'filtered angular rate'],
              'COLORS': ['blue', 'orange', 'red'],
              'YMIN':0, 'YMAX':0}

iplt.plot(runfunct, int(10**initial_value), sliderparams, plotparams, sliderfunct)