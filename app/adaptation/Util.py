from app.Util import get_output_folder_for_latest_EPOS_run


class Util:

    @classmethod
    def get_trip_overheads(cls, start_index, index_count):
        end_index = start_index + index_count
        trip_overheads = []
        with open("data/overheads.csv", 'r') as results:
            for i, line in enumerate(results):
                if i >= start_index and i < end_index:
                    trip_overheads.append(float(line.split(",")[6]))
        return trip_overheads

    @classmethod
    def get_street_utilizations(cls, start_index, index_count):
        end_index = start_index + index_count
        utilizations = []

        with open("data/streets.csv", 'r') as results:
            for i, line in enumerate(results):
                line = line.split(",")
                line[len(line)-1] = line[len(line)-1].replace('\r', '').replace('\n', '')
                if i == 0:
                    streets = line
                else:
                    if i > start_index and i <= end_index:
                        utilizations.append([float(u) for u in line[1:]])

        streets_data = {}
        for i in range(len(streets)):
            streets_data[streets[i]] = [utilization[i] for utilization in utilizations]

        return streets_data, streets


    @classmethod
    def get_predicted_street_utilization_in_latest_EPOS_run(cls, steps, street_ids):

        # get 'numIterations' EPOS parameter
        with open("conf/epos.properties", "r") as epos_properties:
            for line in epos_properties:
                if line.startswith("numIterations"):
                    epos_iterations_per_simulation =  int(line.split("=")[1])

        # get predicted utilizations per street per planning step for latest EPOS run by looking at the latest iteration
        with open(get_output_folder_for_latest_EPOS_run() + "/global-response.csv", "r") as results:
            for line_number, line in enumerate(results):
                if line_number == epos_iterations_per_simulation:
                    result = line.split(",")[2:]

        # split predicted utilization list into X list where X is the number of steps
        split_function = lambda A, n: [A[i:i+n] for i in range(0, len(A), n)]
        utilizations = split_function(result, len(street_ids))

        # add keys to the utilizations lists
        predicted_utilizations_per_street_in_planning_steps = list()

        for step_id in range(steps):
            utilizations_in_planning_step = utilizations[step_id]
            utilizations_per_street_in_planning_step = dict()
            street_id = 0
            for street_name in street_ids:
                utilizations_per_street_in_planning_step[street_name] = utilizations_in_planning_step[street_id]
                street_id += 1
            predicted_utilizations_per_street_in_planning_steps.append(utilizations_per_street_in_planning_step)

        return predicted_utilizations_per_street_in_planning_steps