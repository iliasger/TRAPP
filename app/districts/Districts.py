import subprocess
import random
from app.network.Network import Network
import sumolib
import xml.etree.ElementTree as ET
import itertools
from app import Config
import os, sys

# import of SUMO_HOME
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


class Districts(object):

    number_districts = 0
    totalPopulation = 0
    district = None
    accumulated_weight = 0
    total_edges = 0

    @classmethod
    def loadDistricts(cls):

        if (Config.do_gridding):
            Districts.createTazFile()
        else:
            Districts.filldistricts()

    @classmethod
    def createTazFile(cls):
        if(Config.debug):
            print('Loading districts from network into new file')
        #creates a TAZ file with all of the districts and their xy values and their contained edges
        #'-v' for verbose mode, '-n' to provide network, '-o' to provide output file for TAZ, '-w' for width(m) of grid
        process = subprocess.Popen(["python", "/usr/local/Cellar/sumo/1.2.0/share/sumo/tools/district/gridDistricts.py",
                                    '-v',
                                    '-n', (Config.sumoNet),
                                    '-o', Config.taz_file,
                                    '-w', str(Config.districtSize)])
        process.wait()  #need to wait for process so that the taz_file is created before it is opened in createDistrictFile()
        Districts.createDistrictsFile()


    @classmethod
    def createDistrictsFile(cls):

        #starts the new root of an xml to hold the district coordinates and IDs
        districts = ET.Element('districts')
        ET.SubElement(districts, 'number_districts')

        #accessing the TAZ file of grids of the network that was just created with gridDistricts.py
        tazTree = ET.parse(Config.taz_file)
        root = tazTree.getroot()

        if Config.debug:
           print('**If it stops here before converting to geo-coordinates and module pyproj is not found,'
                  'download pyproj with pip install or on git. More info on sumo dlr**')

        #capturing populations from csv file so the file only has to be opened and read once and then
        #the container can be iterated through to add populations to districts
        populations = Districts.computePopulationProbabilities()

        for taz in root.iter('taz'):
            Districts.number_districts = Districts.number_districts + 1
            att = taz.attrib    #capturing the attributes of one TAZ

            x, y, lon, lat, passanger_edges = ([] for i in range(5))

            #isolating the xy coordniates from the 'shape' attribute of each TAZ(district)
            xy = (item for item in att['shape'].split(' '))
            all_edges = (item for item in att['edges'].split(' '))

            #loading in the network to use in converting the coordinates
            net = sumolib.net.readNet(Config.sumoNet)

            #passenger_edges = Districts.isolatePassengerEdges(all_edges)

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

            #initilizing variable to hold the population of the current ditrict as the populations of the zip codes
            #are added into the current district
            popD = 0
            for popZ in populations:
                latZ = float(popZ['lat'])
                lonZ = float(popZ['lon'])
                popZn = float(popZ['pop'])

                #detemining if the centroid of the zip code is within the current district
                if (latZ < lat[2] and latZ > lat[0] and lonZ > lon[0] and lonZ < lon[2]):

                    Districts.totalPopulation=  Districts.totalPopulation + popZn
                    popD = popZn + popD

                    popZ['pop'] = 0 #this just resets the population to 0 when it has been added to a district

            #adding to new .xml file the id and geoCoordinates of each generated district
            ET.SubElement(districts, "district",
                          id=taz.attrib['id'],
                          pop=str(popD),
                          accumulated_weight=str(0),
                          geoCoords=' '.join((str(la) + ',' + str(lo)) for (lo, la) in itertools.izip(lon, lat)),
                          edges=taz.attrib['edges']) #passenger_edges)

        if (Config.debug):
            print(str(Districts.number_districts) + " districts.")

        #writing districts to tree and new file, saving under map directory
        tree = ET.ElementTree(districts)
        root = tree.getroot()

        Districts.district = [{'id':None, 'population_dist':0,
                               'accumulated_weight':0, 'edges':None,
                               'times_chosen':0} for n in range(int(Districts.number_districts + 1))]

        line_count = 0
        accumulating_weight = 0

        for dist in root.iter('district'):
            att = dist.attrib

            #computing the fraction of the population in each district and writing to xml
            population_probability = float(att['pop']) / Districts.totalPopulation
            dist.set('pop', str(population_probability))

            #using accumulating weight when selecting a district to start a vehicle in
            accumulating_weight = accumulating_weight + population_probability
            dist.set('accumulated_weight', str(accumulating_weight))

            Districts.district[line_count] = {'id':att['id'],
                                              'population_dist':att['pop'],
                                              'accumulated_weight':str(accumulating_weight),
                                              'edges':att['edges'],
                                              'times_chosen':0}

            line_count = line_count + 1

        Districts.accumulated_weight = accumulating_weight

        #keeps track of the total values in the xml to use when filling Districts.district without generating new file
        ET.SubElement(districts, 'totals',
                      number_districts=str(Districts.number_districts),
                      max_weight=str(Districts.accumulated_weight))

        tree.write(Config.populated_districts)


    @classmethod
    def computePopulationProbabilities(cls):

        if (Config.debug):
            print('Computing the population probabilities.')

        with open(Config.zipcodes, 'r') as csv_file:
            if (Config.debug):
                print('Reading zipcode csv file')

            line_count = 0

            #reading the zip codes and their populations from the csv file
            for line in csv_file:
                line = line.strip().split(',')
                if line_count == 0:
                    line_count = line_count + 1
                elif line_count == 1:
                    #initializing the container to hold the lat, lon, and pop for each zipcode
                    number_zipcodes = int(line[0])
                    populations = [{'lat':0, 'lon':0, 'pop':0} for n in range(number_zipcodes)]
                    totalPop = line[3]
                    line_count = line_count + 1
                else:
                    populations[line_count - 2] = {'lat':line[1], 'lon':line[2], 'pop':line[3]}
                    line_count = line_count + 1
            if (Config.debug):
                print(str(number_zipcodes) + " zip codes included.")
        return populations


    @classmethod
    def filldistricts(cls):
    #this method fills the container Districts.district when Config.do_districting == False
    #and all of the district files have already been generated on an earlier run

        if(Config.debug):
            print('Loading districts from district file')

        populated_districts_file = ET.parse(Config.populated_districts)
        root = populated_districts_file.getroot()

        totals = root.find('totals').attrib
        Districts.number_districts = int(totals['number_districts'])
        Districts.accumulated_weight = float(totals['max_weight'])

        #initilaization of container to hold the distrits' information
        Districts.district = [{'id':None,
                               'population_dist':0,
                               'accumulated_weight':0,
                               'edges':None,
                               'times_chosen':0} for n in range(int(Districts.number_districts + 1))]


        #filling global district container from file
        district_count = 0
        for populated_district in root.iter('district'):
            att = populated_district.attrib
            Districts.district[district_count] = {'id':att['id'],
                                                  'population_dist':att['pop'],
                                                  'accumulated_weight':att['accumulated_weight'],
                                                  'edges':att['edges'], 'times_chosen':0}
            district_count = district_count + 1


    @classmethod
    def get_nonrandom(cls):
        district_id = Districts.getDistrictID()

        for dist in Districts.district:
            if (dist['id'] ==  district_id):
                edges = dist['edges'].split(' ')
                #select a random edge within the chose district
                edge = random.choice(edges)
                edge = Network.getEdgeByID(edge).getFromNode().getID()
                return edge

        if (Config.debug):
            print('Error no edge selected for route.')
        return None


    @classmethod
    def getDistrictID(cls):
        random.seed()
        random_number = random.random()

        for dist in Districts.district:
            #randomly select a district
            if (random_number <= float(dist['accumulated_weight'])):
                dist['times_chosen'] = str(int(dist['times_chosen']) + 1)
                return dist['id']

        if (Config.debug):
            print('Error no district selected for route.')
        return None


    @classmethod
    def isolatePassengerEdges(cls, all_edges):
        ##if the map is unable to be cleaned and still has edges that are not for passanger vehicles,
        #then this method can be used to ensure that only passenger edges are added to districts
        total = 0
        passenger_edges = []
        for edge in all_edges:
            edge_node = Network.getEdgeByID(edge)
            if(edge_node.allows("passenger")):
                passenger_edges.append(edge)
                total = total + 1

        print("total Passanger edges: " + str(total))
        return " ".join(passenger_edges)


    @classmethod
    def printDistrictDistribution(cls):
        ##for testing purposes to print the number of times each district is chosen for a route
        for dist in Districts.district:
            print("ID: " + str(dist['id']) + " Population Distribution: " + str(dist['population_dist'])
                  + " Times Chosen: " + str(dist['times_chosen']))

    @classmethod
    def testDistrictEdges(cls):
        for dist in Districts.district:
            if (dist['edges'] != None):
                edges = dist['edges'].split(' ')
                length = len(edges)
                Districts.total_edges = Districts.total_edges + length

            print('Total Edges')
            print(Districts.total_edges)