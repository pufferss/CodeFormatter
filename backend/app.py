from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, template_folder='templates')
with open('FlaskKey.dat') as f:
    app.secret_key = f.read()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        options = request.form.to_dict()
        if options['button'] == 'checker':
            print(options['language'])
        else:
            print(options['namingConv'], options['indentConv'], options['spacesConv'])
    print(options)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='5000')