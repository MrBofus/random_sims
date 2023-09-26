
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import random
import pyIGRF
import pyproj
from poliastro.twobody.orbit import Orbit
from poliastro.bodies import Earth
from astropy import units as u

from pyatmos import download_sw_jb2008,read_sw_jb2008
from pyatmos import jb2008

swfile = download_sw_jb2008()
swdata = read_sw_jb2008(swfile) 



def ECI_to_ECEF(r, t):
    
    gamma = (360/(23.9345*3600)) * t
    gamma *= np.pi/180
    
    x = r[0]*np.cos(gamma) - r[1]*np.sin(gamma) # meters
    y = r[0]*np.sin(gamma) + r[1]*np.cos(gamma) # meters
    z = r[2] # meters
    
    transformer = pyproj.Transformer.from_crs({"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
                                              {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'})
    
    lon, lat, alt = transformer.transform(x, y, z, radians=False)
    
    return lon, lat, alt


def indexparser(counter, length):
    
    j = length*np.sin(counter) + int(length/2)

    return int(j)



# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])


length = 100
lat_o = -90
lon_o = -180

x, y = np.meshgrid( np.linspace(lon_o, 180, length), np.linspace(lat_o, 90, length) )


zlist = [ [], [], [], [], [],
          [], [], [], [], [],
          [], [], [],]
l = []

print('\n\n\n\n')
# t = '2014-07-22 22:18:45'
# t = '2022-01-22 21:00:00'
t = '2022-01-23 21:00:00'
for k in range(len(zlist)):
    for i in range(length):
        for j in range(length):

            jb08 = jb2008('2022-01-22 ' + str(10+k) + ':00:00', (y[j][0], x[0][i], 525), swdata)
            l.append(jb08.T)
            
            # bfield = pyIGRF.igrf_variation(y[j][0], x[0][i], 200 + 10*k, 2020)
            # print(bfield[-1])
            # l.append(bfield[-1])
        
        print('\r\033[0;32m\tset ' +str(k+1) + ' of ' + str(len(zlist)) + ', ' + str(int(100*i/length)) + '% complete\033[0;0m', end='')
        zlist[k].append(l)
        l = []

    print('\r\033[0;32m\tset ' +str(k+1) + ' of ' + str(len(zlist)) + ', ' + str(100) + '% complete\033[0;0m\n', end='')



orbit_1 = Orbit.from_classical(Earth, (6378.1 + 525) << u.km, 0.001 << u.one, 22.1 << u.deg, 0 << u.deg, 0 << u.deg, -160 << u.deg)
orbit_2 = Orbit.from_classical(Earth, (6378.1 + 525) << u.km, 0.001 << u.one, 58.6 << u.deg, 0 << u.deg, 0 << u.deg, -160 << u.deg)

sat_lat_1 = []
sat_lon_1 = []

sat_lat_2 = []
sat_lon_2 = []

t = 0
dt = 30
while t < 4600:

    lon_1, lat_1, _ = ECI_to_ECEF((orbit_1.r << u.meter).value, t)
    lon_2, lat_2, _ = ECI_to_ECEF((orbit_2.r << u.meter).value, t)

    sat_lat_1.append(lat_1)
    sat_lon_1.append(lon_1)
    sat_lat_2.append(lat_2)
    sat_lon_2.append(lon_2)

    orbit_1 = orbit_1.propagate(dt << u.second)
    orbit_2 = orbit_2.propagate(dt << u.second)

    t += dt




m = Basemap(projection = 'mill', lon_0 = 0, resolution = 'l')
_ = input('\n\nbegin animation? ')
for i in range(1000):
    ax.clear()

    m.drawcoastlines()
    m.fillcontinents()


    # draw parallels
    m.drawparallels(np.arange(-90, 90, 20), labels=[1, 1, 0, 1])
    # draw meridians
    m.drawmeridians(np.arange(-180, 180, 30), labels=[1, 1, 0, 1])

    m.pcolormesh(x, y, zlist[i%len(zlist)], latlon=True, cmap='RdBu_r', alpha=0.5)

    sat_lon_plots_1, sat_lat_plots_1 = m(sat_lon_1, sat_lat_1)
    sat_lon_plots_2, sat_lat_plots_2 = m(sat_lon_2, sat_lat_2)
    m.plot(sat_lon_plots_1, sat_lat_plots_1, marker=None, color='b')
    m.plot(sat_lon_plots_2, sat_lat_plots_2, marker=None, color='r')

    ax.set_title(str(i+1) + '')
    plt.pause(0.01)