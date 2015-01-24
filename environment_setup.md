# Setting Up Your Local Environment

The following commands help you to set up your environment to contribute to the project on github. Pay attention to whether you have activated virtual environments when installing certain packages.

**Note: Everything here is for a Mac Running OS 10.9. Setting up other environments will require some Googling.**

## Install Foundational Tools

### XCode

Install XCode and command line tools: http://developer.apple.com/downloads

### Homebrew

A tool to assist with further installs of packages

    ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go/install)"

### GCC

Required for Numpy/Pandas, which handle our calculations

    brew install gcc

    # If that doesn't work, try `brew install gfortran`

### PIP

Python package manager (https://pypi.python.org/pypi/pip). Allows us to quickly install packages that assist with calculations, etc.

    sudo easy_install pip


## Get the Code from Github

The url of the repo is https://github.com/npinger/pensioncalc

Follow the instructions for [forking a repo](https://help.github.com/articles/fork-a-repo/)

## Install Virtual Environment Manager and Create Evironment

Virtual environments allow you to create isolated spaces on your computer so multiple projects' packages don't conflict with each other. For details, read [this description](http://www.silverwareconsulting.com/index.cfm/2012/7/24/Getting-Started-with-virtualenv-and-virtualenvwrapper-in-Python).

### Installation

    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    mkdir ~/.virtualenvs

Teach the shell to read from/write to the active virtual environment

    # Open ~/.bash_profile
    sudo nano ~/.bash_profile

    # nano is a text editor for mac
    # See http://guides.macrumors.com/nano for details

    # Add these lines to the file you opened/created
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

    # Press ctrl + x to exit nano

Now run the ~/.bash_profile file so the command line knows to use it

    source ~/.bash_profile

### Create the Virtual Environment

    # Make the new virtualenv
    mkvirtualenv --distribute pensioncalc

    # To enter the pensioncalc virtualenv
    workon pensioncalc

    # To exit pensioncalc virtualenv
    deactivate

YOU WANT TO BE INSIDE THE VIRTUAL ENVIRONMENT FOR ALL FUTURE INSTALLATIONS

i.e. Whenever you run a line that starts with `pip install`, make sure that you are in the virtualenv. You can tell by looking at the command line:

    # To see the difference, type in the shell
    deactivate

    # Then type
    workon pensioncalc

    # Should see this difference:
    # Command line when you are in the virtualenv
    (pensioncalc)<some info about your file path or user>$

    # Command line when you are not in the virtualenv
    <some info about your file path or user>$


## Setting up Virtual Environment

Note: You should make sure that you have typed `workon pensioncalc` before running the following commands, and that the virtual environment is active (see above for details.)

### Install iPython (Optional)

This is an augmented python shell that makes development/debugging easier

    pip install ipython

### Install Requrements files

NOTE: YOU MUST COMPLETE THE "Get the Code from Github" STEP BEFORE RUNNING THESE COMMANDS

You must install the base_requirements.txt before installing requirements.txt (because requirements.txt has packages that depend on those in base_requirements.txt).

    # First run
    pip install -r /sites/pensioncalc/confs/base_requirements.txt

    # Be sure to check for errors before moving on! Google errors if you find them.

    # Then run
    pip install -r /sites/pensioncalc/confs/requirements.txt
