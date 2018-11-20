# Orb
A simple chat-bot system

## Installation
* Getting the code `git clone https://github.com/Bijan-Ghasemi-Afshar/Orb.git`
* Creating a virtual environment `py -3 -m venv venv`
* Using the virtual environment
    * If using **Powershell**
        1. Close the window and reopen it with administration privilages
        2. Run `set-executionpolicy remotesigned` and Respond `Y`
        3. Close and reopen the Powershell in the project and the run `venv\Scripts\activate`
    * If using **Unix-like terminal**
        1. run `. venv\bin\activate`
* Getting required python packages
    * Make sure **pip** is installed then run `pip install -r requirements.txt`
* Getting the javascript packages
    * Make sure **Nodejs** & **npm** are installed
    * Navigate to **orb/static**
    * Run `npm install` to install javascript packages
    * Then run `npm run build` to bundle javascript & css