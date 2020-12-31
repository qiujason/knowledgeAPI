from flask import Flask, request, jsonify
import json
import PDFDocSummarization

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return make_error('No file in request')
    file = request.files


@app.route('/', methods=['POST'])
def hello_world():
    data = json.loads(request.data)
    if 'text' not in data:
        return make_error('No text in request')
    highlights = PDFDocSummarization.article_to_summary(data['text'], 4)
    return json.dumps(highlights)


def make_error(message):
    resp = jsonify({'message': message})
    resp.status_code = 400
    return resp


if __name__ == '__main__':
    app.run()
