""" Helper functions """
import os, shutil


def addToAverage(totalCount, totalValue, newValue):
    """ simple sliding average calculation """
    return ((1.0 * totalCount * totalValue) + newValue) / (totalCount + 1)


def get_output_folder_for_latest_EPOS_run():
    current_max = 0
    for name in os.listdir("output"):
        output_number = int(name.split("_")[1])
        if output_number > current_max:
            current_max = output_number
    output_folder_for_latest_EPOS_run = "output/plans_" + str(current_max)
    print "latest EPOS output in " + output_folder_for_latest_EPOS_run
    return output_folder_for_latest_EPOS_run


def add_data_folder_if_missing():
    if not os.path.exists("data"):
        os.makedirs("data")


def remove_overhead_and_streets_files():
    if os.path.exists("data/overheads.csv"):
        os.remove("data/overheads.csv")
    if os.path.exists("data/streets.csv"):
        os.remove("data/streets.csv")

def prepare_epos_input_data_folders():
    if not os.path.exists("datasets"):
        os.makedirs("datasets")

    if os.path.exists("datasets/plans"):
        plans_folder = os.listdir("datasets/plans")
        for item in plans_folder:
            if item.endswith(".plans"):
                os.remove("datasets/plans/" + item)
    else:
        os.makedirs("datasets/plans")

    if os.path.exists("datasets/routes"):
        shutil.rmtree("datasets/routes")
    os.makedirs("datasets/routes")
