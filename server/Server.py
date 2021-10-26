import os
from flask import Flask,flash,request,redirect,url_for
from werkzeug.utils import secure_filename
from wificheck import check_network

UPLOAD_FOLDER = '/home/pi/Desktop/SeniorProject/MVP/Upload'
ALLOWED_EXTENSIONS = {'csv'}

def main():
    server()

def server():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = 'many random bytes'

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/', methods = ['GET','POST'])
    def upload_file():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('no file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                temp_file = check_network()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_file + '.csv'))
                flash('Thank you')
                return redirect(request.url)
                #return redirect(url_for('upload_file', name=filename))
                #return 'Thank you'

        return '''
        <!doctype html>
        <title> Upload Network csv File</title>
        <h1> Upload Network csv File</h1>
        <form method = post enctype=multipart/form-data>
            <input type = file name = file>
            <input type = submit value = Upload>
        </form>
        '''

    #if __name__ == '__main__':
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')



if __name__ == '__main__':
    main()
