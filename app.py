import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import json
import WebScraping
import SiteSummarization
import PDFDocSummarization
import PDFtoText

UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './' + UPLOAD_FOLDER


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':  # site query
        return json.dumps(WebScraping.web_scraping(request.args.get('website')))
    elif request.method == 'POST':
        if 'file' in request.files:  # pdf upload
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file = request.files['file']
            if file.filename == '':
                return make_error('No file selected')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            highlights = ''
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                file.save(filepath)
                highlights = json.dumps(PDFDocSummarization.article_to_summary(PDFtoText.pdf_to_text(filepath), 4))
                os.remove(filepath)
            if highlights == '':
                return make_error('Invalid file')
            return highlights
        elif 'text' in request.get_json():  # text upload
            return json.dumps(PDFDocSummarization.article_to_summary(request.get_json()['text'], 4))
        else:
            return make_error('Invalid request')


def make_error(message):
    resp = jsonify({'message': message})
    resp.status_code = 400
    return resp


if __name__ == '__main__':
    app.run()
