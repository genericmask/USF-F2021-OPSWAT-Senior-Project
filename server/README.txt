This was made following (some of) the Flask tutorial: https://flask.palletsprojects.com/en/2.0.x/tutorial/

Setup steps from https://flask.palletsprojects.com/en/2.0.x/installation/
and https://flask.palletsprojects.com/en/2.0.x/quickstart/

Initial setup steps macOS/Linux:
1. Open a terminal in the server folder.
2. Create a venv folder with "python3 -m venv venv"
3. Activate the environment with ". venv/bin/activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install flask with "pip install Flask"
5. Install twilio with "pip install twilio"
6. Initialize environment variables: 
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
7. Initialize the database by running: "flask init-db"
   You should see "Initialized the database."
8. Start flask:
    $ flask run --host=0.0.0.0

Initial setup steps Windows:
1. Open a cmd prompt in the server folder.
2. Create a venv folder with "py -3 -m venv venv"
3. Active the environment with "venv\Scripts\activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install flask with "pip install Flask"
5. Install twilio with "pip install twilio"
6. Initialize environment variables: 
    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
7. Initialize the database by running: "flask init-db"
   You should see "Initialized the database."
8. Start flask:
     > flask run

To re-initialize the db:
1. Follow steps 1, 3, 6, and 7 of initial setup for your OS

To run the server after initial setup:
1. Follow steps 1, 3, 6, and 8 of initial setup for your OS

To start the pinger:
1. Do steps 1 and 3 of initial setup for your OS
2. Run the pinger.py file

Notes:
"--host=0.0.0.0" broadcasts the webpage to the network your device is on. This allows you to connect to the webpage from a 
different device by putting in the host device ip address and port into your web browser.
