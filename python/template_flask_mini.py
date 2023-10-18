from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/hello_template')
def toto():
    return render_template('hello.html', msg='<br>titi<br>')


if __name__ == '__main__':
    app.run(debug=True, port=5050)

