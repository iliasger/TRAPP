from numpy import mean

class Util:

    overheads_index = 0
    streets_index = 0

    @classmethod
    def calculate_trip_overheads(cls):
        trip_overheads = []
        with open("data/overheads.csv", 'r') as results:
            for i, line in enumerate(results):
                if i >= cls.overheads_index:
                    trip_overheads.append(float(line.split(",")[6]))

            overheads_index_increment = len(trip_overheads)
            cls.overheads_index += overheads_index_increment
        return trip_overheads

    @classmethod
    def calculate_street_utilizations(cls):
        utilizations = []
        with open("data/streets.csv", 'r') as results:
            for i, line in enumerate(results):
                line = line.split(",")
                line[len(line)-1] = line[len(line)-1].replace('\r', '').replace('\n', '')
                if i == 0:
                    streets = line
                else:
                    if i > cls.streets_index:
                        utilizations.append([float(u) for u in line[1:]])
            streets_index_increment = len(utilizations)
            cls.streets_index += streets_index_increment

        streets_data = {}
        for i in range(len(streets)):
            streets_data[streets[i]] = [utilization[i] for utilization in utilizations]

        streets_utilizations = {}
        for key, value in streets_data.iteritems():
            streets_utilizations[key] = mean(value)

        return streets_utilizations