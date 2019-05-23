# TRAPP
TRAPP framework for Traffic Reconfiguration via Adaptive Participatory Planning
<!--The user guide for the SEAMS 2019 reviewers is available at https://www4.in.tum.de/~gerostat/SEAMS19_user_guide.zip.-->

## Read about TRAPP
* [Pre-print](http://wwwbroy.in.tum.de/~gerostat/pubs/SEAMS19-EPOS-SUMO.pdf) of TRAPP publication at the [14th Symposium on Software Engineering for Adaptive and Self-Managing Systems 2019](https://conf.researchr.org/home/seams-2019)

## Installation

1. Download and install the latest version [SUMO](https://sumo.dlr.de/wiki/Installing) (v1.2.0).

	* On debian or ubuntu, SUMO can be installed simply via:

		```
		sudo add-apt-repository ppa:sumo/stable
		sudo apt-get update
		sudo apt-get install sumo sumo-tools sumo-doc
		```

	* On Mac OSX we recommend using Homebrew:

		```
		brew tap dlr-ts/sumo
		brew install sumo
		```

	* If you have to build SUMO from source using these commands:

		```
	    sudo apt-get install -y build-essential git libxerces-c-dev
	    sudo mkdir -p /opt && sudo cd /opt
	    sudo git clone https://github.com/radiganm/sumo.git
	    sudo cd /opt/sumo && sudo ./configure
	    sudo cd /opt/sumo && sudo make
	    sudo cd /opt/sumo && sudo make install
		```

1. Set `SUMO_HOME` environment variable the folder of your SUMO intallation.
	* Hint: If SUMO is installed via the regular distribution in debian/ubuntu, it is installed at `/usr/share/sumo`.

1. Clone the latest TRAPP version from github via `git clone https://github.com/iliasger/TRAPP.git`

1. Navigate to the newly created TRAPP folder.

1. If `setuptools` are not installed in your system, [install](https://pypi.org/project/setuptools/) them.

1. Install the python dependencies of TRAPP by issuing (inside the newly created TRAPP folder): `python setup.py install`

1. Download the [0.0.1 release of EPOS](https://github.com/epournaras/EPOS/releases/tag/0.0.1) and unzip it. Note the path to the path in the unzipped folder.

1. Open the file `app/Config.py` inside the TRAPP project in an editor of your choice and set the value of the `epos_jar_path` variable to the above path.

## Troubleshooting

If you need help in using or extending TRAPP, feel free to contact us:

* [Ilias Gerostathopoulos](http://wwwbroy.in.tum.de/~gerostat/), <gerostat@in.tum.de>
* [Evangelos Pournaras](http://evangelospournaras.com/), <epournaras@ethz.ch>