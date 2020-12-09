# P2-analyse-de-marché

*This repository hosts a project to achieve during my training OpenClassRooms.com*

This script was created on Python 3.9.

The purpose of this script is to extract information of each books of the website <http://books.toscrape.com/>.

A .CSV file is created for each category in the `./csv/` repertory, and each image is saved on `./img/` repertory.

## Installation

Download the files in the directories of your choice

### 1) Create a Virtual Environment :
 
Go to the directory where you downloaded files and run this command on your terminal:

    python3 -m venv env
    
Then, initialize it :
 
- On Windows, run:

        tutorial-env\Scripts\activate.bat
    
- On Unix or MacOS, run:

        source tutorial-env/bin/activate
        
For more information, refer to the python.org documentation :

<https://docs.python.org/3/tutorial/venv.html>
    
### 2) Install the requirements

Still on you terminal, with the environment activated, run the following command to install the required libraries
    
    pip install -r requirements
    
### 3) Run the script

You can run the script using this command :

    python script.py
    
    