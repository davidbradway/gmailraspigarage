# RaspiGmail checker for garage opener

- need a filter that labels incoming messages that meet some critera with the label 'garage'
- when a new message gets labeled that way, if it came from the address listed in the python script, then activate the door

## Installation

To run the script are required Python and Nmap, which can be found at the following : 

* https://www.python.org/downloads/

* http://nmap.org/download.html

Also, take a look here : https://pypi.python.org/pypi/python-nmap

    wget https://pypi.python.org/packages/source/p/python-nmap/python-nmap-0.3.4.tar.gz
    tar xvfz python-nmap-0.3.4.tar.gz 
    rm python-nmap-0.3.4.tar.gz 
    wget https://github.com/mpescimoro/WiFinder/archive/master.zip
    unzip master.zip 
    rm master.zip 
    sudo apt-get install nmap
