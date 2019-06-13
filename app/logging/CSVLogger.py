import csv, os

from app import Config
from app.adaptation import Knowledge
# unclear if need ^ this try with config first, otherwise have to change the name of files

csv.register_dialect('custom', doublequote=False, quoting=csv.QUOTE_NONE)


def logEvent(file, row):
    try:
        #if statement to heck if alpha or beta strategies as if they are want
        # to store the overheads file eleswhere
        if file=='beta' or file =='alpha':
            with open('./results/' + str(Config.resultsFolder) +'/'+ str(file)+ '/' + '_a'+ str(Knowledge.alpha)+
                      '_b' + str(Knowledge.beta) + '_s' + str(Config.random_seed) +
                      '.csv', 'ab') as mycsvfile:
                writer = csv.writer(mycsvfile, dialect='excel')
                writer.writerow(row)
        else :
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