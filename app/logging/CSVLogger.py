import csv, os

from app import Config

csv.register_dialect('custom', doublequote=False, quoting=csv.QUOTE_NONE)


def logEvent(file, row):
    try:
        with open('./data/' + str(file) + '.csv', 'ab') as mycsvfile:
            writer = csv.writer(mycsvfile, dialect='excel')
            writer.writerow(row)
    except:
        pass

def log_baseline_result(file, row):
    try:
        results_folder = "results/baseline/" + str(Config.totalCarCounter)
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        with open(results_folder + '/' + str(file) + '_' + str(Config.processID) + '.csv', 'ab') as mycsvfile:
            writer = csv.writer(mycsvfile, dialect='excel')
            writer.writerow(row)
    except:
        pass