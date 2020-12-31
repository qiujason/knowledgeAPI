from flask import Flask, request
import json
import PDFDocSummarization

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    data = json.loads(request.data)
    highlights = PDFDocSummarization.article_to_summary(data['text'], 4)
    return json.dumps(highlights)


if __name__ == '__main__':
    app.run()
