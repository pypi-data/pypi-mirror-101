
# superpower-gui
> This application provides a graphical wrapper to access functions in the superpower R pacakge.


## Latest Release
### ANOVA




![png](docs/images/output_1_0.png)



## Previous
### Correlation and Chi Squared



        <iframe
            width="400"
            height="300"
            src="https://www.youtube.com/embed/5cNr5Dvzvrs"
            frameborder="0"
            allowfullscreen
        ></iframe>
        


## Run the Development Version on MyGeoHub

1. Log into https://mygeohub.org
2. Go to https://mygeohub.org/tools/superpower/
3. Click the "Launch Tool" button


![png](docs/images/output_6_0.png)


## Installing superpower-gui

Installing the superpower-gui locally is pretty straight forward with one exception. The SuperPower R package needs to be installed on your machine, and Python needs to know where to find your prefered version of R. In most cases, superpower_gui will install it for you, but if you have trouble you may need to install it on your own and use a config file to specify its location.

### Installing from PyPi

`pip install superpower-gui`

### Installing From Source

`git clone https://github.rcac.purdue.edu/brewer36/superpower_gui.git`

`cd superpower_gui`

`pip install superpower_gui`

## Installing SuperPower R Package

### From Github

This application does not run without the companion R package, Superpower. You can install it any way you like. The application will check every library location listed by `.libPaths`. If the package isn't installed, the application can do that for you, but you must provide the path to the package source file. Since the package doesn't release these yet, so you will have to create one by building it from the original repository.

```bash
git clone https://github.rcac.purdue.edu/brewer36/SuperPower.git`
R CMD build SuperPower
R CMD INSTALL Superpower_<version>.tar.gz
```

### From a source file

Open ~/.superpower_gui/config.ini source file. You can optionally provide a library location if you'd like the source file to be installed in a particular place.

```
['R']
source = <source_dir>
lib_loc = <optional_lib_loc>
```

## How to use

This application runs in a single cell of a Jupyter Notebook, or an Javascript enabled IPython environment.

```
#hide_output
from superpower_gui.controller import Controller

controller = Controller()
controller
```
