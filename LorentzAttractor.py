import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import random



def LorenzDiff(x, y, z,
               sigma, rho, beta):
    dxdt = sigma*(y - x)
    dydt = x*(rho - z) - y
    dzdt = x*y - beta*z

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
                       gap, linewidth, gradient):
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

        axes.plot(x[i-1:i+gap], y[i-1:i+gap], z[i-1:i+gap], c=colorcode, linewidth=linewidth, alpha=gradient)





def return_a_bright_color():
    will_it_be_three_or_two_or_one = 6*(1 - random.random())

    if will_it_be_three_or_two_or_one < 1:
        b1 = 1 - random.random()/2
        d1 = random.random()/2
        d2 = random.random()/2

        c = [b1, d1, d2]
        random.shuffle(c)

        return c

    elif will_it_be_three_or_two_or_one < 2:
        b1 = 1 - random.random()/2
        b2 = 1 - random.random()/2
        d1 = random.random()/2

        c = [b1, b2, d1]
        random.shuffle(c)

        return c
    
    else:
        b1 = 1 - random.random()/2
        b2 = 1 - random.random()/2
        b3 = 1 - random.random()/2

        return [b1, b2, b3]


def return_a_dark_color():
    return [random.random()/2, random.random()/2, random.random()/2]








fig = plt.figure(facecolor='black')
ax = plt.axes(projection='3d')

fig.canvas.toolbar.pack_forget()
plt.rcParams['toolbar'] = 'None'
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()







while True:
    x, y, z = 2, 2, 2

    x, y, z = 5*random.random()+0.5, 5*random.random()+0.5, 5*random.random()+0.5

    # sigma = 10
    # rho = 28
    # beta = 8/3

    sigma = 10 # + (1-random.random())
    rho = 28 # + (1-random.random())
    beta = 8/3 # + 0.5*(1-random.random())


    c1 = return_a_bright_color()
    c2 = return_a_dark_color()


    t = 0
    dt = 0.005

    df = pd.DataFrame()
    counter = 0
    while True:
        tempdf = pd.DataFrame({'t':[t], 'x':[x], 'y':[y], 'z':[z]})
        df = pd.concat([df, tempdf])



        if counter % 15 == 0:
            ax.clear()

            '''
            ax.plot( np.array(df['x'].tail(100000)), np.array(df['y'].tail(100000)), np.array(df['z'].tail(100000)), 
                            color='white')
            '''

            
            plot_with_gradient(ax, c1, c2,
                                np.array(df['x'].tail(50000)), 
                                np.array(df['y'].tail(50000)), 
                                np.array(df['z'].tail(50000)),
                                int(len(df)/10 + 1), 1, 1)
            plot_with_gradient(ax, c1, c2,
                                np.array(df['x'].tail(50000)), 
                                np.array(df['y'].tail(50000)), 
                                np.array(df['z'].tail(50000)),
                                int(len(df)/2 + 1), 5, 0.3)
            

            ax.set_axis_off()

            ax.set_facecolor("black")
            ax.set_aspect('equal')

            plt.pause(0.001)



        dxdt, dydt, dzdt = LorenzDiff(x, y, z, 
                                        sigma, rho, beta)
        x, y, z = integrate(x, y, z, 
                            dxdt, dydt, dzdt,
                            dt)

        t += dt
        counter += 1

        if t > 100:
            break
        