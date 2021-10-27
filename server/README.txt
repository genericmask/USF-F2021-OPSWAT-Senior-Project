This was made following (some of) the Flask tutorial: https://flask.palletsprojects.com/en/2.0.x/tutorial/

Setup steps from https://flask.palletsprojects.com/en/2.0.x/installation/
and https://flask.palletsprojects.com/en/2.0.x/quickstart/

Setup steps macOS/Linux:
1. Open a terminal in the server folder.
2. Create a venv folder with "python3 -m venv venv"
3. Activate the environment with ". venv/bin/activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install flask with "pip install Flask"
5. To start flask, run: 
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask run

Setup steps Windows:
1. Open a cmd prompt in the server folder.
2. Create a venv folder with "py -3 -m venv venv"
3. Active the environment with "venv\Scripts\activate". Your shell prompt wil change to
    show the name of the activated environment.
4. Install flask with "pip install Flask"
5. To start flask, open Powershell and run:
    > $env:FLASK_ENV = "development"
    > flask run