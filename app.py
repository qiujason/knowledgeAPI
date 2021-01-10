from flask import Flask, request, jsonify
import json
import WebScraping
import Summarization
import PDFtoText

UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './' + UPLOAD_FOLDER


@app.route('/upload_site', methods=['GET'])
def upload_site():
    if request.args.get('website'):
        return Summarization.site_article_to_summary(WebScraping.web_scraping(request.args.get('website')), 20)
    return make_error('No website')


@app.route('/upload_text', methods=['POST'])
def upload_text():
    if request.get_json() and 'text' in request.get_json():  # text upload
        return json.dumps(Summarization.pdf_article_to_summary(request.get_json()['text'], 4))


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' in request.files:  # pdf upload
        file = request.files['file']
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            highlights = json.dumps(Summarization.pdf_article_to_summary(PDFtoText.pdf_to_text(file), 4))
            if highlights == '':
                return make_error('Invalid file')
            return highlights
    return make_error('No file uploaded or file not named \'file\'')


def make_error(message):
    resp = jsonify({'message': message})
    resp.status_code = 400
    return resp


if __name__ == '__main__':
    app.run()
