''' API for a simple text board.
'''

from flask import Flask

app: Flask = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'


# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)