import DEVisualizer as dev
import random

'''
params = [10, 28, 8/3]
initial_params = 5*random.random()+0.5, 5*random.random()+0.5, 5*random.random()+0.5

def funct(params, x, y, z, t):
    sigma, rho, beta = params[0], params[1], params[2]

    dxdt = sigma*(y - x)*y
    dydt = x*(rho - z) - y
    dzdt = x*y - beta*z*z

    return dxdt, dydt, dzdt
'''



b11 = 2
F1m = 1/3
b12 = 0.7933
F2m = -1
b13 = 0.1914
F3m = 1
b21 = 1.19
L1m = 0
b22 = 3.215
L2m = 0
b31 = 0.5742
L3m = 22.8
b33 = 5.8
b32 = 0

params = [b11, b12, b13, 
          b21, b22, 0,
          0, b32, b33,
          F1m, F2m, F3m,
          L1m, L2m, L3m]

initial_params = [0.1, 0.1, 0.1]


def funct(params, x, y, z, t):
    b11, b12, b13 = params[0], params[1], params[2]
    b21, b22, b23 = params[3], params[4], params[5]
    b31, b32, b33 = params[6], params[7], params[8]

    F1m, F2m, F3m = params[9], params[10], params[11]
    L1m, L2m, L3m = params[12], params[13], params[14]

    dxdt = -b11*x - b12*y + b13*z + F1m*y*z + L1m
    dydt =  b21*x + b22*y         + F2m*x*z + L2m
    dzdt = -b32*x - b33*z         + F3m*x*y + L3m   

    return dxdt, dydt, dzdt



dt = 0.005
buffer = 15
timeout = 100
dev.visualizeDE(funct, params, initial_params, dt, buffer, timeout)