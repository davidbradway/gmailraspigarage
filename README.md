# RaspiGmail checker for garage opener

- Create a filter that labels incoming messages that meet some critera with the label 'garage'
- When a new message gets labeled that way, check if it came from the address listed in the python script
- Begin checking the local network for the presence of device(s) that are whitelisted
- If the device is seen within the specified period, then activate the door opener

## Installation

To run the script, the dependencies are Python and Nmap, which can be found at the following : 
- https://www.python.org/downloads
- http://nmap.org/download.html
- Also, take a look here: https://pypi.python.org/pypi/python-nmap
- Commands:

    wget https://pypi.python.org/packages/source/p/python-nmap/python-nmap-0.3.4.tar.gz
    tar xvfz python-nmap-0.3.4.tar.gz 
    rm python-nmap-0.3.4.tar.gz 

    sudo apt-get install nmap

    wget https://github.com/mpescimoro/WiFinder/archive/master.zip
    unzip master.zip 
    rm master.zip 

    git clone git@bitbucket.org:davidbradway/gmailraspigarage.git

    sudo cp raspigmail.sh /etc/init.d/
    sudo chmod 755 /etc/init.d/raspigmail.sh 
    sudo update-rc.d raspigmail.sh defaults
    # If you ever want to remove the script from start-up, run the following command:
    sudo update-rc.d -f raspigmail.sh remove

    sudo /etc/init.d/raspigmail.sh start
    sudo /etc/init.d/raspigmail.sh status
    sudo /etc/init.d/raspigmail.sh stop

    sudo crontab -e
    # Add this to CRON
    # m h  dom mon dow   command
    #*/1 * * * * /home/pi/repos/raspigmail/autorestart.sh
