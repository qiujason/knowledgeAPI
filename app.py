from flask import Flask, request

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def hello_world():
    data = request.data
    return data

if __name__ == '__main__':
    app.run()
