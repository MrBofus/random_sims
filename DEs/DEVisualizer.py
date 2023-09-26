import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import random

##````````````````````````````````````````````````````````````````````````````````````````````##

def rk4(funct, params,     x, y, z,    t, h):
    
    k1x, k1y, k1z = h*funct(params, x,y,z,t)[0], \
                    h*funct(params, x,y,z,t)[1], \
                    h*funct(params, x,y,z,t)[2]

    k2x, k2y, k2z = h*funct(params, x+k1x/2,y+k1y/2,z+k1z/2,t+h/2)[0], \
                    h*funct(params, x+k1x/2,y+k1y/2,z+k1z/2,t+h/2)[1], \
                    h*funct(params, x+k1x/2,y+k1y/2,z+k1z/2,t+h/2)[2]

    k3x, k3y, k3z = h*funct(params, x+k2x/2,y+k2y/2,z+k2z/2,t+h/2)[0], \
                    h*funct(params, x+k2x/2,y+k2y/2,z+k2z/2,t+h/2)[1], \
                    h*funct(params, x+k2x/2,y+k2y/2,z+k2z/2,t+h/2)[2]

    k4x, k4y, k4z = h*funct(params, x+k3x,y+k3y,z+k3z,t+h)[0], \
                    h*funct(params, x+k3x,y+k3y,z+k3z,t+h)[1], \
                    h*funct(params, x+k3x,y+k3y,z+k3z,t+h)[2]

    return x+(k1x+2*k2x+2*k3x+k4x)/6, \
           y+(k1y+2*k2y+2*k3y+k4y)/6, \
           z+(k1z+2*k2z+2*k3z+k4z)/6

##````````````````````````````````````````````````````````````````````````````````````````````##

def interpolate_between_colors(color1, color2, i):
    return i*np.array(color1) + (1-i)*np.array(color2)

##````````````````````````````````````````````````````````````````````````````````````````````##

def plot_with_gradient(axes, c1, c2,
                       x, y, z,
                       gap, linewidth, gradient):
    
    for i in range(1, len(x), gap):
        iterator = i/len(x)

        colorcode = interpolate_between_colors(c1, c2, iterator)

        axes.plot(x[i-1:i+gap], y[i-1:i+gap], z[i-1:i+gap], c=colorcode, linewidth=linewidth, alpha=gradient)

##````````````````````````````````````````````````````````````````````````````````````````````##

def simple_spin(axes, theta, omega, timestep):
    elev, azim = theta[0], theta[1]
    vx, vy = omega[0], omega[1]

    elev = elev + vx*timestep
    azim = azim + vy*timestep

    if elev > 360:
        elev = 0
    elif elev < -360:
        elev = 0

    axes.view_init(elev=elev, azim=azim)

    return [elev, azim], [vx, vy]

##````````````````````````````````````````````````````````````````````````````````````````````##

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

##````````````````````````````````````````````````````````````````````````````````````````````##

def return_a_dark_color():
    return [random.random()/2, random.random()/2, random.random()/2]

##````````````````````````````````````````````````````````````````````````````````````````````##

fig = plt.figure(facecolor='black')
ax = plt.axes(projection='3d')

fig.canvas.toolbar.pack_forget()
plt.rcParams['toolbar'] = 'None'
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()


omega = [62.5*(2*random.random() - 1), 62.5*(2*random.random() - 1)]
theta = [180*random.random(), 180*(2*random.random()-1)]

##````````````````````````````````````````````````````````````````````````````````````````````##

def visualizeDE(funct, params, initial_params, dt, framerate, timeout):

    while True:
        x, y, z = initial_params

        omega = [62.5*(2*random.random() - 1), 62.5*(2*random.random() - 1)]
        theta = [180*random.random(), 180*(2*random.random()-1)]

        c1 = return_a_bright_color()
        c2 = return_a_dark_color()

        t = 0

        df = pd.DataFrame()
        counter = 0
        while True:
            tempdf = pd.DataFrame({'t':[t], 'x':[x], 'y':[y], 'z':[z]})
            df = pd.concat([df, tempdf])

            if counter % framerate == 0:
                ax.clear()

                theta, omega = simple_spin(ax, theta, omega, dt)


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


            x, y, z = rk4(funct, params, x, y, z, t, 0.005)

            t += dt
            counter += 1

            if t > timeout:
                break

'''
params = [10, 28, 8/3]
initial_params = 5*random.random()+0.5, 5*random.random()+0.5, 5*random.random()+0.5
dt = 0.005
framerate = 15
timeout = 100

def funct(params, x, y, z, t):
    sigma, rho, beta = params[0], params[1], params[2]

    dxdt = sigma*(y - x)
    dydt = x*(rho - z) - y
    dzdt = x*y - beta*z

    return dxdt, dydt, dzdt

visualizeDE(funct, params, initial_params, dt, framerate, timeout)
'''