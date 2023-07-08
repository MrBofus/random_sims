import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import random



def GeneralizedChuaCircuit(x, y, z,
                            alpha, beta, gamma):
    
    # alpha = 9
    # beta = 14.286
    # gamma = 0

    dxdt = alpha * (y - h(x))
    dydt = x - y + z
    dzdt = -beta*y - gamma*z

    return dxdt, dydt, dzdt

def h(x):
    m0 = -1/7
    m1 = 2/7
    m2 = -4/7
    m3 = 2/7
    m4 = -4/7
    m5 = 2/7

    b1 = 1
    b2 = 2.15
    b3 = 3.6
    b4 = 8.2
    b5 = 13

    # n = 3

    term1 = m5*x

    term2 = 0.5 * (m0 - m1)*(abs(x + b1) - abs(x - b1))
    term3 = 0.5 * (m1 - m2)*(abs(x + b2) - abs(x - b2))
    term4 = 0.5 * (m2 - m3)*(abs(x + b3) - abs(x - b3))
    term5 = 0.5 * (m3 - m4)*(abs(x + b4) - abs(x - b4))
    term6 = 0.5 * (m4 - m5)*(abs(x + b5) - abs(x - b5))

    return term1 + term2 + term3 + term4 + term5 + term6



def ThomasCylindrical(x, y, z,
                      b):
    dxdt = np.sin(y) - b*x
    dydt = np.sin(z) - b*y
    dzdt = np.sin(x) - b*z

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
    x, y, z = -2, 2, -2

    # x, y, z = 5*random.random()+0.5, 5*random.random()+0.5, 5*random.random()+0.5

    # sigma = 10
    # rho = 28
    # beta = 8/3

    sigma = 9       # 10 # + (1-random.random())
    rho = 14.286    # + (1-random.random())
    beta = 0        # + 0.5*(1-random.random())

    b = 0.208186


    c1 = return_a_bright_color()
    c2 = return_a_dark_color()


    t = 0
    dt = 0.005 * 5

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



        dxdt, dydt, dzdt = ThomasCylindrical(x, y, z, 
                                                b)
        x, y, z = integrate(x, y, z, 
                            dxdt, dydt, dzdt,
                            dt)

        t += dt
        counter += 1

        if t > 100:
            break
        