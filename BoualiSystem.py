import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import random



def function(x, y, z,
                    a, b, c, d, h):
    dxdt = a*x*(1-y) - b*z
    dydt = -c*y*(1-x**2)
    dzdt = h*x

    return dxdt, dydt, dzdt

def integrate(x, y, z,
              dxdt, dydt, dzdt, 
              dt):
    x = x + dxdt * dt
    y = y + dydt * dt
    z = z + dzdt * dt

    return x, y, z


def interpolate_between_colors(color1, color2, i):
    return i*np.array(color1) + (1-i)*np.array(color2)


def plot_with_gradient(axes, c1, c2,
                       x, y, z,
                       gap):
    '''
    for i in range(1, len(x)):
        colorcode = [ 1 - abs(t[i-1]/max(t)), 
                     1, 
                     1 ]
        axes.plot(x[i-1:i+1], y[i-1:i+1], z[i-1:i+1], c=colorcode)
    '''
    
    for i in range(1, len(x), gap):
        '''
        iterator = abs(t[i]/max(t)) ** 0.5
        if iterator > 1: iterator = 0.999999
        '''

        iterator = i/len(x)

        '''
        colorcode = interpolate_between_colors([0.9607, 0.9843, 0.1764], 
                                               [0.5725, 0.0000, 0.5843], iterator)
        '''
        '''
        colorcode = interpolate_between_colors([0.9999, 0.9999, 0.1764], 
                                               [0.4000, 0.0000, 0.4000], iterator)
        '''

        colorcode = interpolate_between_colors(c1, c2, iterator)

        axes.plot(x[i-1:i+gap], y[i-1:i+gap], z[i-1:i+gap], c=colorcode)





def sim(x, y, z, t, counter):
    pass









fig = plt.figure(facecolor='black')
ax = plt.axes(projection='3d')

fig.canvas.toolbar.pack_forget()
plt.rcParams['toolbar'] = 'None'
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()







while True:
    x, y, z = 1, 1, 0

    # x, y, z = 5*random.random(), 5*random.random(), 5*random.random()

    # sigma = 10
    # rho = 28
    # beta = 8/3

    a = 3
    b = 2.2
    c = 1
    d = 0
    h = 0.001

    c1 = [random.random(), random.random(), random.random()]
    c2 = [random.random(), random.random(), random.random()]

    t = 0
    dt = 0.01

    df = pd.DataFrame()
    counter = 0
    while True:
        tempdf = pd.DataFrame({'t':[t], 'x':[x], 'y':[y], 'z':[z]})
        df = pd.concat([df, tempdf])



        if counter % 60 == 0:
            ax.clear()

            '''
            ax.plot( np.array(df['x'].tail(100000)), np.array(df['y'].tail(100000)), np.array(df['z'].tail(100000)), 
                            color='white')
            '''

            
            plot_with_gradient(ax, c1, c2,
                            np.array(df['x'].tail(50000)), 
                            np.array(df['y'].tail(50000)), 
                            np.array(df['z'].tail(50000)),
                            int(len(df)/10 + 1))
            

            ax.set_axis_off()

            ax.set_facecolor("black")
            #ax.set_aspect('equal')

            plt.pause(0.001)



        dxdt, dydt, dzdt = function(x, y, z,
                                            a, b, c, d, h)
        x, y, z = integrate(x, y, z, 
                            dxdt, dydt, dzdt,
                            dt)

        t += dt
        counter += 1

        if t > 1000:
            break
        