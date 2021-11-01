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
6. To start flask, run: 
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask run --host=0.0.0.0

Initial setup steps Windows:
1. Open a cmd prompt in the server folder.
2. Create a venv folder with "py -3 -m venv venv"
3. Active the environment with "venv\Scripts\activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install flask with "pip install Flask"
5. Install twilio with "pip install twilio"
6. To start flask, run:
    > set FLASK_APP=flaskr
    > flask run

To initialize the db:
1. Follow steps 1 and 3 of initial setup for your system.
2. Set the environment variables:
    macOS: 
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development

    Powershell:
    > $env:FLASK_ENV = "development"

3. Run: "flask init-db"
   You should see "Initialized the database."

To run the server after initial setup:
1. Do steps 1, 3, & 5 for your OS

Notes:
"--host=0.0.0.0" broadcasts the webpage to the network your device is on. This allows you to connect to the webpage from a 
different device by putting in the host device ip address and port into your web browser.
