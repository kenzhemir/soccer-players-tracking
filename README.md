# soccer_players_tracking
Detection and tracking of the soccer players


## Installation guide

**Install the following requirements**  
Anaconda or Miniconda
**Get the code**
Clone or download github repository:  
```
git clone --recursive https:github.com/kenzhemir/soccer_players_tracking
```  

**Setup the environment**  
Create conda environment using environment.yml file
provided in repository:
```
cd soccer_players_tracking
conda env create -f environment.yml -p ./env
```
New environment will be created in the env folder.  
Activate the environment:  
```
source activate path/to/soccer_players_tracking/env
```
**Install darkflow**  
In soccer_players_tracking folder
```
pip install ./darkflow
```

**Configure parameters**  
In main.py edit host, port and detection frequency vari-
ables  

**Run the code**  
```
python main.py
```

## Having trouble with installation?

Write me a message -> miras.kenzhegaliyev@nu.edu.kz