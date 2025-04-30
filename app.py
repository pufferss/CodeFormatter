from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__, template_folder='templates')
with open('FlaskKey.dat') as f:
    app.secret_key = f.read()
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='5000')