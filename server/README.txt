Works with Python 3.9.5 and (possibly?) 3.7.x

This was made following (some of) the Flask tutorial: https://flask.palletsprojects.com/en/2.0.x/tutorial/

Setup steps from https://flask.palletsprojects.com/en/2.0.x/installation/
and https://flask.palletsprojects.com/en/2.0.x/quickstart/

Initial setup steps macOS/Linux:
1. Open a terminal in the server folder.
2. Create a venv folder with "python3 -m venv venv"
3. Activate the environment with ". venv/bin/activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install dependencies with "pip install Flask twilio WTForms phonenumbers"
5. Initialize environment variables: 
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
6. Initialize the database by running: "flask init-db"
   You should see "Initialized the database."
7. Start flask:
    $ flask run --host=0.0.0.0

Initial setup steps Windows:
1. Open a cmd prompt in the server folder.
2. Create a venv folder with "py -3 -m venv venv"
3. Active the environment with "venv\Scripts\activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install dependencies with "pip install Flask twilio WTForms phonenumbers"
5. Initialize environment variables: 
    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
6. Initialize the database by running: "flask init-db"
   You should see "Initialized the database."
7. Start flask:
     > flask run

To re-initialize the db:
1. Follow steps 1, 3, 5, and 6 of initial setup for your OS

To run the server after initial setup:
1. Follow steps 1, 3, 5, and 7 of initial setup for your OS

To start the pinger:
1. Do steps 1 and 3 of initial setup for your OS
2. Run the pinger.py file

Notes:
"--host=0.0.0.0" broadcasts the webpage to the network your device is on. This allows you to connect to the webpage from a 
different device by putting in the host device ip address and port into your web browser.
