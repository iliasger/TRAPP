from app.adaptation.Strategy import Strategy
from app.adaptation.Util import *
from app.adaptation import Knowledge
from app import Config
from app.adaptation import Util
import os

#this class can be used when running exp_beta.py and exp_alpha.py

class Beta(Strategy):

    # add_overhead_results_folder_if_missing:
    # Checks to see if 4 folders exist and if not creates them:
    #   1. City Folder: adds the folder for the new city(name specified by Config.results_folder)
    #       in the results folder
    #   2. Alpha or beta folder: add the folder with in the new city folder
    #   3. Global and (4)Local folder: add the new folders to the alpha or beta folder
    def add_overhead_results_folder_if_missing(self,alpha_or_beta):
        path="results/"+ str(Config.resultsFolder)
        abpath= str(path) + '/'+ str(alpha_or_beta)
        global_path = str(path) + '/' + str(alpha_or_beta) + "/global"
        local_path = str(path) + '/' + str(alpha_or_beta) + "/local"

        #checking to see if Config.results_folder path exist,
        # then alpha or beta folder paths exist (depending on what is calling it,
        # then local and global folder,
        # if they do not exist create a new folder
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(abpath):
            os.makedirs(abpath)
        if not os.path.exists(global_path):
            os.makedirs(global_path)
        if not os.path.exists(local_path):
            os.makedirs(local_path)

    # get_constants:
    # Gets the last line of the global-const.csv and local-const.csv
    # of the plans folder just created by epos for that run and returns the last line
    @staticmethod
    def get_constants(self, global_local):
        # want global_local input to only be "global" or "local"
        plans = Util.get_output_folder_for_latest_EPOS_run()
        names= plans + '/' +global_local + '-cost.csv'
        file= open(names,'r')
        lineList= file.readlines()
        file.close()
        last_line = lineList[len(lineList) - 1]
        # to test uncomment the line below in order to print the last line
        # print "The last line is: "+ last_line
        return last_line


    # new_file_for_const:
    # Calls get_constants and grab last line of both global-const.csv and local-const.csv
    # and put in new individual file
    # the file format should be found within resultsFolder created with the specific city name
    # the file format should be "local_a#_b#_s#" and "global_a#_b#_s#",
    # a- alpha and the # for that run
    # b- beta and the # for that run
    # s- seed and the # for that run
    # the run of simulation in EPOS
    def new_file_for_cost(self,alpha_or_beta):
        #gets output folder path for most recent epos run
        plan_num= Util.get_output_folder_for_latest_EPOS_run()

        # get the number correlating with plans so easier to compare, only want number for testing if correct
        # makes harder to grab data for graphs
        #num_only= plan_num[len(plan_num)-10:len(plan_num)]

        #the new file for the global cost and local cost last line
        globalcost = Beta.get_constants(self, 'global')
        localcost = Beta.get_constants(self,'local')

        path= './results/' + str(Config.resultsFolder) + '/'+ str(alpha_or_beta)

        #creating local cost file for that run/plan
        # if want to see number of plans add str(num_only) to the string of name
        with open(path + '/local/' + 'local_a' + str(Knowledge.alpha) +
                  '_b' + str(Knowledge.beta) + '_s' + str(Config.random_seed) + 
                  '.csv', 'w') as mycsvfilelocal:
            mycsvfilelocal.write(localcost)
            mycsvfilelocal.close()

        #creating the global cost file for that run/plan
        # if want to see number of plans add str(num_only) to the string of name
        with open(path +'/global/' + 'global_a' + str(Knowledge.alpha) +
                  '_b' + str(Knowledge.beta) + '_s' + str(Config.random_seed) +
                  '.csv', 'w') as mycsvfileglobal:
            mycsvfileglobal.write(globalcost)
            mycsvfileglobal.close()







