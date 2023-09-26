
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pyproj
from poliastro.twobody.orbit import Orbit
from poliastro.bodies import Earth
from astropy import units as u

'''
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


# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])


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

m.drawcoastlines()
m.fillcontinents()

# draw parallels
m.drawparallels(np.arange(-90, 90, 20), labels=[1, 1, 0, 1])
# draw meridians
m.drawmeridians(np.arange(-180, 180, 30), labels=[1, 1, 0, 1])

sat_lon_plots_1, sat_lat_plots_1 = m(sat_lon_1, sat_lat_1)
sat_lon_plots_2, sat_lat_plots_2 = m(sat_lon_2, sat_lat_2)
m.plot(sat_lon_plots_1, sat_lat_plots_1, marker=None, color='b')
m.plot(sat_lon_plots_2, sat_lat_plots_2, marker=None, color='r')

plt.show()
'''


def indexparser(counter, length):
    
    if counter % 2*length > length:
        return counter % length
    else:
        return length - counter%length


print('\n')
for i in range(30):
    print(indexparser(i, 10))