import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_PATH = 'uploaded_files/'
ALLOWED_EXTENTIONS = {'c', 'cpp', 'py'}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

with open('FlaskKey.dat') as f:
    app.secret_key = f.read()

def SaveUploadedFile():
        if 'input-file' in request.files:
            file = request.files['input-file']
            if file.filename == '':
                raise ValueError('Vous devez upload un fichier')
            if not file.filename.split('.')[1] in ALLOWED_EXTENTIONS:
                raise ValueError('mauvaise extention')
            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) POUR REMOVE LE FILE DU SERV

                return filename
        else:
            raise ValueError('Vous devez upload un fichier')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        options = request.form.to_dict()
        #print(options['namingConv'], options['indentConv'], options['spacesConv'])
        print(options)
        try:
            filename = SaveUploadedFile()
            print(filename)
        except ValueError as e:
            return f'{e}'
    return render_template('index.html')

@app.route('/checker', methods=['GET', 'POST'])
def checker():
    dico = {
        'PascalCase' : 0,
        'camelCase' : 0,
        'lowercase' : 0,
        'Unknown' : 0,
    }
    if request.method == 'POST':
        options = request.form.to_dict()
        checkbox = True if 'lang-checkbox' in options else False
        try:
            filename = SaveUploadedFile()
            print(filename)
        except ValueError as e:
            return f'{e}'
    return render_template('checker.html', data=list(dico.values()), labels = list(dico.keys()))

@app.route('/obfuscator', methods=['GET', 'POST'])
def obfuscator():
    return render_template('obfuscator.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='5000')