##````````````````````````````````````````````````````````````````````````````````````````````````##
# Let's get filtering!
#
# import libraries
#   numpy - general math library, used to generate a sine wave and random numbers
#   matplotlib - plotting library, used to visualize how well our filter did
import numpy as np
import matplotlib.pyplot as plt

##````````````````````````````````````````````````````````````````````````````````````````````````##
# define some useful funcions

# real gyro measurements
#   takes in simulation time
#   returns real angular rate measurement
def real_gyro_measurement(t):
    return 10*np.sin(0.5*t)

# pull gyro measurements
#   takes in real angular rate measurement
#   returns real meaasurement plus sensor noise
def pull_gyro_measurement(w):
    return w + np.random.normal(0, 3)

# low pass filter
#   takes in list of previous measurements, with the first 
#         element being the first measurement and the 
#         last element being the most recent measurement, also 
#         takes in window size. Note: higher window size means 
#         lower errors, but greater amount of lag behind true angular rate.
#         Try altering this value between '3' and '100' to see the difference.
#         A good value seems to be 20.
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


##````````````````````````````````````````````````````````````````````````````````````````````````##
# initialize parameters

# size of window for low-pass fiter.
#   Note: lowering this value means the filtered data will have high noise with low latency,
#         increasing this value means the filtered data will have low noise with high latency.
#   
#         The goal is to find an optimum value for this using the real sensor and trying varying
#         window sizes until noise is low enough with acceptably high latency.
size_of_window = 20

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


##````````````````````````````````````````````````````````````````````````````````````````````````##
# making the plots

# tell matplotlib you want all graphs on one figure
plt.figure(1)

# plot the measured, real, and filtered results
plt.plot(times, angular_rates_measured, label='measured angular rate')
plt.plot(times, angular_rates_real, label='true angular rate')
plt.plot(times, angular_rates_filtered, c='red', label='filtered data')

# add a grid and a legend to the plot
plt.grid()
plt.legend()

# show the figure
plt.show()