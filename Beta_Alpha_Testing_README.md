# TRAPP City-Scale Alpha Beta Testing
TRAPP framework for Traffic Reconfiguration via Adaptive Participatory Planning
<!--The user guide for the SEAMS 2019 reviewers is available at https://www4.in.tum.de/~gerostat/SEAMS19_user_guide.zip.-->

## Read about TRAPP
* [Pre-print](http://wwwbroy.in.tum.de/~gerostat/pubs/SEAMS19-EPOS-SUMO.pdf) of TRAPP publication at the [14th Symposium on Software Engineering for Adaptive and Self-Managing Systems 2019](https://conf.researchr.org/home/seams-2019)

## Installation and Set Up

1. Follow the steps for downloading [TRAPP](https://github.com/iliasger/TRAPP/tree/experiments#trapp), which can be found in the general README.

1. Once TRAPP is correctly installed, create a `app/Config.py` file using `app/Config_TEMPLATE.py` as a guide. Copy `Config_TEMPLATE.py` into `app/Config.py` and fill in any information under the `#TODO` label.

1. Creating a new map for the desired city.

	* Using the command line, maneuver to the tools folder found within SUMO and use the following command to open OSM Web Wizard : `python osmWebWizard.py`
	* Once in OSM Web Wizard: enter the coordinates of the desired city, configue the shape of the box, and hit the generate simulation button.
	* The associated files are saved in a folder under tools with the format YYYY-MM-DD-HH-MM-SS and the only files necessary to run the new city are osm.net.xml, osm.sumo.cfg, and osm.view.xml all of which can renamed.
	* To clean up the map, use the command `netedit`, open the .net.xml file of the map, and delete any unnecessary roads.
	* To remove all edges except passenger edges, maneuver to the folder that holds the map and use the command `netconvert -s “app/map/Example.net.xml” -o “app/map/Example.net.xml” --keep-edges.by-vclass “passenger” --tls.guess-signals --tls.discard-simple --tls.join`
	* In the Config.py file, set `sumoConfig` equal to the path containing the `sumo.cfg` file and set `sumoNet` equal to the path containing the `.net.xml` file.
	* Now the new map should be able to run in TRAPP.

1. Use the Districting by ZIP code Step-by-Step Instructions found in the general README.md for more accurte origin selection. 

	After `app/map/CityNameDistricts/CityName_districts.xml` is created keep the *use_districts* paramter as *True* and the *do_gridding* as *False* in `app/Config.py`. 

1. run baseline ( show what the config file should look like) with `exp_baseline_overheads.py` ( and show/tell what want that file to look like , the uses has teh option of how many baseline want)  

1. Repeat steps 3-5 for each desired city.

## Running the Experiment 
For these steps it is assumed that the appropriate district files have been created for the city being used, the baseline is correctly set up

1. run the `exp__beta.py` and `exp_alpha.py` (explain what should look like and how the name per the city should be the same in each run)

1. can talk about what data each `exp__beta.py` and `exp_alpha.py` collects from the plan 

1. the data collected where used to create 6 distinct graphs

1. talk about the jupyter notebools that can be used to recreate teh graphs used 


## Troubleshooting

If you need help in extending TRAPP or adding new cities and their district in the experiment, feel free to contact us:

* Brionna Davis, <brionna.e.davis@vanderbilt.edu>
* Grace Jennings, <grace.e.jennings@vanderbilt.edu>
* Taylor Pothast, <taylor.m.pothast@vanderbilt.edu>
* Ilias Gerostathopoulos <gerostat@in.tum.de>
