import subprocess
from app.network.Network import Network
from app import Config
import sumolib
import xml.etree.ElementTree as ET
import itertools
#import district

from app import Config
#from app.routing.RoutingEdge import RoutingEdge

import os, sys

# import of SUMO_HOME
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


class Districts(object):

    @classmethod
    def loadDistricts(cls):

        #this creates a TAZ file with all of the districts and their xy values and their contained edges
        #'-v' for verbose mode, '-n' to provide network, '-o' to provide output file for TAZ, '-w' for width
        process = subprocess.Popen(["python", "/usr/local/Cellar/sumo/1.2.0/share/sumo/tools/district/gridDistricts.py",
                                    '-v',
                                    '-n', "/Users/gracejennings/TRAPP/app/map/eichstaedt.net.xml",
                                    '-o', "/Users/gracejennings/TRAPP/app/map/taz_file.taz.xml",
                                    '-w', str(Config.districtSize)])

        #this starts the new root of an xml to hold the district coordinates and IDs
        districts = ET.Element('districts')

        #accessing the TAZ file of grids of the network that was just created with gridDistricts.py
        tazTree = ET.parse('app/map/taz_file.taz.xml')
        root = tazTree.getroot()

        if Config.debug:
            print('If it stops here before converting to geocoordinates and module pyproj is not found,'
                  'dowload pyproj with pip install or on git.  More info on sumo dlr')

        #looping through each TAZ (traffic assignment zone) in the folder
        for taz in root.iter('taz'):
            #capturing the attributes of one TAZ
            att = taz.attrib
            #initliazing lists to hold xy coordinates to find geoCoords
            x = []
            y = []
            lon = []
            lat = []
            #isolating the needed xy coodniates from the 'shape' attribute
            xy = (item for item in att['shape'].split(' '))
            net = sumolib.net.readNet(Config.sumoNet)
            for values in xy:
                #captures each x and y value and adds to the appropriate list
                xn = float(values.split(',')[0])
                yn = float(values.split(',')[1])
                x.append(xn)
                y.append(yn)
                #converting to geocoordinates and passing in the appropriate parsed network
                nlon, nlat = sumolib.net.Net.convertXY2LonLat(net, xn, yn)
                lon.append(nlon)
                lat.append(nlat)

            if Config.debug:
                print('Attempting to convert the coordinates of districts into long,lat')
                print('x values:')
                print(x)
                print('y values:')
                print(y)
                print('longitute values:')
                print(lon)
                print('latitude values:')
                print(lat)

            #adding to new .xml file the id and geoCoordinates of each generated district
            ET.SubElement(districts, "district",
                          geoCoords=' '.join((str(lo) + ',' + str(la)) for (lo, la) in itertools.izip(lon, lat)),
                          id=taz.attrib['id'])

        #writing districts to tree and new file, saving under map directory
        tree = ET.ElementTree(districts)
        tree.write('app/map/taz_coord.taz.xml')

        Districts.getEdgesInDistrict()


    @classmethod
    def getEdgesInDistrict(cls):

        process = subprocess.Popen(["python", "/usr/local/Cellar/sumo/1.2.0/share/sumo/tools/edgesInDistricts.py",
                                    '-v',
                                    '-n', "/Users/gracejennings/TRAPP/app/map/eichstaedt.net.xml",
                                    '-t', "/Users/gracejennings/TRAPP/app/map/taz_file.taz.xml",
                                    '-o', "/Users/gracejennings/TRAPP/app/map/districts.taz.xml",
                                    '-i'])

    @classmethod
    def computePopulationProbabilities(cls):

