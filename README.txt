endpointsIP.csv contains a sample CSV endpoints list which would be uploaded to the NAC checker.

File Structure:
The folder "server" contains all the files needed to run the NAC checker software.
In "server" is the folder "flaskr" which contains the Flask app and its associated files.
In "flaskr" are the folders:
* "static" which contains css for the webpage.
* "templates" which contains the HTML templates the Flask app uses to build the webpage.
* "validators" which contains a Python module used for user input validation.

Works with Python 3.X.X >= 3.7

Initial setup steps macOS/Linux:
1. Open a terminal in the server folder.
2. Create a venv folder with "python3 -m venv venv"
3. Activate the environment with ". venv/bin/activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install dependencies with "pip install Flask twilio WTForms phonenumbers turbo_flask"
5. Initialize environment variables: 
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
6. Initialize the database by running: "flask init-db"
   You should see "Initialized the database."
7. Start flask:
    $ flask run --host=0.0.0.0
8. Start the pinger:
    $ python3 pinger.py

Initial setup steps Windows:
1. Open a cmd prompt in the server folder.
2. Create a venv folder with "py -3 -m venv venv"
3. Active the environment with "venv\Scripts\activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install dependencies with "pip install Flask twilio WTForms phonenumbers turbo_flask"
5. Initialize environment variables: 
    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
6. Initialize the database by running: "flask init-db"
   You should see "Initialized the database."
7. Start flask:
    > flask run
8. Start the pinger:
    > python3 pinger.py

To re-initialize the db:
1. Follow steps 1, 3, 5, and 6 of initial setup for your OS

To run the server after initial setup:
1. Follow steps 1, 3, 5, and 7 of initial setup for your OS

To start the pinger:
1. Do steps 1 and 3 of initial setup for your OS
2. Run the pinger.py file

To run as docker container on Linux:
1. Open a terminal in the server folder.
2. Build the image.
    > sudo docker build -t nacchecker .
3. Run the container.
    > sudo docker run --name nac -d -p 5000:5000 nacchecker:latest

To run as docker container on Windows:
1. Install docker desktop
2. Open cmd in the server folder.
3. Build the image.
    > docker build -t nacchecker .
4. Run the container.
    > docker run --name nac -d -p 5000:5000 nacchecker:latest

Notes:
"--host=0.0.0.0" broadcasts the webpage to the network your device is on. This allows you to connect to the webpage from a 
different device by putting in the host device ip address and port into your web browser.
