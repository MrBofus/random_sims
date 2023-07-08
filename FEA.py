import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def fermiFunction(t, tc, k):
    term = np.exp(t-tc)/(k) + 1
    return 1-1/term


def inRadius(v1, v2, r):
    m_ = magnitude( v2 - v1 )
    if m_ < r:
        return True
    return False


def magnitude(vec):
    mag = 0
    for v in vec:
        mag += v**2
    
    return np.sqrt(mag)


def normalize(vec):
    m = magnitude(vec)
    
    if not m == 0:
        v_ = []
        for v in vec:
            v_.append(v/m)
        
        return v_
    
    else:
        return [0, 0]




def computeDrag(b, c, dA, windspeed, element):
    v_direction = np.array(normalize( element.velocity ))
    v_magnitude = magnitude( element.velocity )
    
    w_direction = np.array(normalize( windspeed ))
    w_magnitude = windspeed
    
    F_d_v = -b * dA * (v_magnitude**2) * v_direction
    F_d_w = -c * dA * (w_magnitude**2) * w_direction
    
    return F_d_v + F_d_w


def compute_normal_stress(k, dl, 
                          elementList, i):
    
    direction1 =     normalize( elementList[i-1].position - elementList[i].position )
    length1 =        magnitude( elementList[i-1].position - elementList[i].position )
    spring1 =        -k * (dl - length1) * np.array(direction1)
    
    direction2 =     normalize( elementList[i].position - elementList[i+1].position )
    length2 =        magnitude( elementList[i].position - elementList[i+1].position )
    spring2 =        k * (dl - length2) * np.array(direction2)
    
    return spring1 + spring2

def compute_normal_stress_final(k, dl, 
                                elementList):
    
    direction =     normalize( elementList[-2].position - elementList[-1].position )
    length =        magnitude( elementList[-2].position - elementList[-1].position )
    spring =        -k * (dl - length) * np.array(direction)
    
    return spring


def compute_shear_stress(k, dl,
                         elementList, i):
    
    direction1 =     normalize( elementList[i-1].position - elementList[i].position )
    direction2 =     normalize( elementList[i+1].position - elementList[i].position )
    
    angle = np.arccos( np.dot(direction1, direction2) )
    
    torque = -k * (np.pi - angle)
    
    Fx = torque * dl
    Fy = torque * dl
    
    return np.array([Fx, Fy])




def check_which_side(elementList, container, i):
    
    # if container.lower_wall < elementList[i].position[1] < container.upper_wall:
    #        if container.lower_wall < elementList[i].position[0] < container.right_wall:
    
    for i in range(len(container.grid)):
        for j in range(len(container.grid)):
            
            if inRadius( container.grid[i][j], elementList[i].position, 0.1):
                
                
                dist_x_r = abs(elementList[i].position[0] - container.right_wall)
                dist_x_l = abs(elementList[i].position[0] - container.left_wall)
                dist_y_u = abs(elementList[i].position[1] - container.upper_wall)
                dist_y_l = abs(elementList[i].position[1] - container.lower_wall)

                '''
                if dist_x_r < 0.05 and dist_y_u < 0.05:
                    return 'xr', 'yu'
                
                elif dist_x_l < 0.05 and dist_y_u < 0.05:
                    return 'xl', 'yu'
                
                elif dist_x_r < 0.05 and dist_y_l < 0.05:
                    return 'xr', 'yl'
                
                elif dist_x_l < 0.05 and dist_y_l < 0.05:
                    return 'xl', 'yl'
                '''
                
                distances = [dist_x_r, dist_x_l, dist_y_u, dist_y_l]
                
                if dist_x_r == min(distances):
                    return 'xr', '0'
                    
                elif dist_x_l == min(distances):
                    return 'xl', '0'
                    
                elif dist_y_u == min(distances):
                    return '0', 'yu'
                    
                elif dist_y_l == min(distances):
                    return '0', 'yl'
    
    return '0', '0'
                    



def compute_external_forces(elementList, forceList, container):
    for i in range(len(elementList)):
        
        side_x, side_y = check_which_side(elementList, container, i)
        
        if side_x == 'xr':
            forceList[i-1][0] = forceList[i-1][0] - forceList[i][0]
            forceList[i][0] = 0
        
        elif side_x == 'xl':
            forceList[i-1][0] = forceList[i-1][0] + forceList[i][0]
            forceList[i][0] = 0
        
        if side_y == 'yu':
            forceList[i-1][1] = forceList[i-1][1] - forceList[i][1]
            forceList[i][1] = 0
        
        elif side_y == 'yl':
            forceList[i-1][1] = forceList[i-1][1] + forceList[i][1]
            forceList[i][1] = 0

    return forceList


def account_for_normal_force(elementList, forceList, container, rest):
    for i in range(len(elementList)):
        
        side_x, side_y = check_which_side(elementList, container, i)
        
        if side_x == 'xr':
            elementList[i].velocity[0] = 0 # -1 * rest * elementList[i].velocity[0]
        
        elif side_x == 'xl':
            elementList[i].velocity[0] = 0 # -1 * rest * elementList[i].velocity[0]
        
        if side_y == 'yu':
            elementList[i].velocity[1] = 0 # -1 * rest * elementList[i].velocity[1]
        
        elif side_y == 'yl':
            elementList[i].velocity[1] = 0 # -1 * rest * elementList[i].velocity[1]

    return elementList


class box():
    def __init__(self, b, s):
        self.lower_wall = b[0]
        self.upper_wall = b[1]
        self.left_wall = s[0]
        self.right_wall = s[1]
        
        size = 10
        
        xm = (self.right_wall - self.left_wall) / size
        ym = (self.upper_wall - self.lower_wall) / size
        
        grid = np.array([0])*(size + 1)
        for i in range(size + 1):
            
            yi = self.lower_wall + i*ym
            
            rj = np.array([0])*(size + 1)
            for j in range(size + 1):
                xj = self.left_wall + j*xm
                
                
                rj[j] = np.array([xj, yi])
            
            grid[i] = rj
        
        self.grid = grid



class element():
    def __init__(self, rxi, ryi, vxi, vyi):
        self.position = np.array([rxi, ryi])
        self.velocity = np.array([vxi, vyi])
 

class rope():
    def __init__(self, l, n, k, kt, ck, cd, m, t, anchorpoint, angle, windspeed, container, rest):
        self.dl = l/n
        self.m = m
        self.dm = m/n
        self.l = l
        self.n = n
        self.k = k
        self.kt = kt
        self.cd = cd
        self.ck = ck
        
        self.t = t
        self.windspeed = windspeed
        
        self.dA = self.dl * self.t
        
        rxi = anchorpoint[0]
        ryi = anchorpoint[1]
        elementList = []
        for i in range(n):
            elementList.append(element(rxi, ryi, 0, 0))
            
            rxi += self.dl * np.cos(angle * np.pi / 180)
            ryi -= self.dl * np.sin(angle * np.pi / 180)
        
        self.elementList = elementList
        
        self.container = container
        self.rest = rest
    
    
    def computeForces(self):
        
        forces = [[0, 0]]
        for i in range(1, len(self.elementList)-1):
            
            gravity = -(self.dm) * 9.81 * np.array([0, 1])
            drag = computeDrag(self.ck, self.cd, self.dA, self.windspeed, self.elementList[i])
            
            intra_normal = compute_normal_stress(self.k, self.dl, self.elementList, i)
            # intra_shear = compute_shear_stress(self.kt, self.dl, self.elementList, i)
            intra_shear = np.array([0, 0])
            
            forces.append( gravity + drag + intra_normal + intra_shear )
        
        gravity = -(self.dm) * 9.81 * np.array([0, 1])
        drag = computeDrag(self.ck, self.cd, self.dA, self.windspeed, self.elementList[-1])
        
        intra_normal = compute_normal_stress_final(self.k, self.dl, self.elementList)
        
        forces.append( gravity + drag + intra_normal )
        
        forces = compute_external_forces(self.elementList, forces, self.container)
        
        self.forces = forces
    
    
    
    def updatePosition(self, vanch, dt):
        
        self.elementList = account_for_normal_force(self.elementList, self.forces, self.container, self.rest)
        
        for i in range(1, len(self.elementList)):
            etemp = self.elementList[i]
            
            vx = etemp.velocity[0] + self.forces[i][0] * dt / self.dm
            vy = etemp.velocity[1] + self.forces[i][1] * dt / self.dm
            
            self.elementList[i] = element(etemp.position[0], etemp.position[1], vx, vy)
        
        
        self.elementList[0] = element(self.elementList[0].position[0], 
                                      self.elementList[0].position[0], 
                                      vanch[0], vanch[1])
        
        for i in range(0, len(self.elementList)):
            etemp = self.elementList[i]
            
            rx = etemp.position[0] + etemp.velocity[0] * dt
            ry = etemp.position[1] + etemp.velocity[1] * dt
            
            
            if i == 0: ry = 0
            # if i == len(self.elementList)-1: rx, ry = 10, 0
            
            self.elementList[i] = element(rx, ry, etemp.velocity[0], etemp.velocity[1])
    
    def updateWindspeed(self, windspeed):
        self.windspeed = windspeed


l = 10
n = 150
k = 2.0*10000
kt = 0
ck = 100
cd = 8
m = 55

th = 0.5

anchorpoint = np.array([0, 0])
vanch = np.array([0, 0])
angle = 55.0

windspeed = np.array([0, 0])

container = box([-12, -8], [-3, 0])
rest = 0.1

myRope = rope(l, n, k, kt, ck, cd, m, th, anchorpoint, angle, windspeed, container, rest)


fig, ax = plt.subplots() 


dt = 0.0025
t = 0
while t < 300:
    ax.clear()
    
    myRope.computeForces()
    myRope.updatePosition(vanch, dt)
    myRope.updateWindspeed(windspeed)
    
    
    # vx = 10*fermiFunction(t, 2, 0.001)
    # vanch = np.array([vx, 0])
    
    windspeed = np.array([10, 0])
    
    '''
    for i in range(1, len(myRope.elementList) ):
        x = [ myRope.elementList[i-1].position[0],
              myRope.elementList[i].position[0] ]
        y = [ myRope.elementList[i-1].position[1],
              myRope.elementList[i].position[1] ]
        ax.plot(x, y, color='b')
    '''
    
    x = []
    y = []
    for e in myRope.elementList:
        x.append(e.position[0])
        y.append(e.position[1])
    
    ax.plot(x, y, color='blue')
    
    
    title = 'c = ' + str(ck) + 'p, th = ' + str(th) + 'm, m = ' + str(m) + 'kg\n\n'
    title += 't = ' + str(int(t)) + 's\n'
    title += 'windspeed: ' + str(round(magnitude(windspeed), 1)) + 'm/s\n'
    title += 'tail speed: ' + str( round(magnitude(myRope.elementList[-1].velocity), 1) ) + 'm/s\n'
    
    ax.set_title(title)
    
    xc = myRope.elementList[0].position[0]
    xl = max( abs(np.array(x)) )
    
    if xl > 15+xc:
        tr = xl - 15 - xc
        tl = 0
    elif xl < -15+xc:
        tr = 0
        tl = xl + 15 - xc
    else:
        tr = 0
        tl = 0
    
    ax.set_xlim([-15+xc+tl, 15+xc+tr])
    ax.set_ylim([-15, 2])
    ax.set_aspect('equal')
    
    plt.pause(0.001)
    t += dt