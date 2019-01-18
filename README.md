# Orb
A simple chat-bot system for booking tickets and predicting estimated arrival time based on journey delay

## Requirements
1. Python 3.6
    * pip (Package Manager)
    * conda (Package Manager)
2. MongoDB
3. NodeJS
    * npm (Package Manager)


## Installation
* **Source Code**
```
git clone https://github.com/Bijan-Ghasemi-Afshar/Orb.git
```
* Creating a **Virtual Environment**
```
conda create -n orbAI
```
* Using the **Virtual Environment**
    * *Linux* & *MacOS*
    ```
    source activate orbAI
    ```
    * *Windows*
    ```
    activate orbAI
    ```
* Getting required **Python Packages**
    ```
    conda install -r requirements1.txt
    ```
    ```
    pip install -r requirements2.txt
    ```
* Getting the **Javascript Packages**
    * Make sure **Nodejs** & **npm** are installed
    * Navigate to **Orb/orb/static**
    ```
    npm install
    npm run build
    ```
* Populating the **Database**
    * *Train stations*: navigate to project **root (Orb/)**
    ```
    python scripts/populate_train_stations.py
    ```
    * *Historical data*: navigate to project **root (Orb/)**
    ```
    python scripts/historical_data.py
    ```

## Running
* Navigate to **Orb/**
* For *Linux* and *Mac*
    * Run `export FLASK_APP=orb`
    * Run `export FLASK_ENV=development`
    * Run `flask run`
    * In browser navigate to **localhost:5000**
* For *Windows cmd*
    * Run `set FLASK_APP=orb`
    * Run `set FLASK_ENV=development`
    * Run `flask run`
    * In browser navigate to **localhost:5000**
* For *Windows PowerShell*
    * Run `$env:FLASK_APP = "orb"`
    * Run `$env:FLASK_ENV = "development"`
    * Run `flask run`
    * In browser navigate to **localhost:5000**