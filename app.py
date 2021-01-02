import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import json
import PDFDocSummarization
import PDFtoText

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './' + UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return make_error('No file in request')
    file = request.files['file']
    if file.filename == '':
        return make_error('No file selected')
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(filepath)
        return json.dumps(PDFDocSummarization.article_to_summary(PDFtoText.pdf_to_text(filepath), 4))
    return make_error('Invalid file')


def make_error(message):
    resp = jsonify({'message': message})
    resp.status_code = 400
    return resp


if __name__ == '__main__':
    app.run()
