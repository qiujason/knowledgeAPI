from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import json
import WebScraping
import Summarization
import PDFtoText

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("localhost", "root", "json1025", "knowledge")
cursor = connection.cursor()


@app.route('/upload_site', methods=['GET'])
def upload_site():
    if request.args.get('website'):
        site = request.args.get('website')
        site_text = WebScraping.web_scraping(request.args.get('website'))
        highlights = Summarization.site_article_to_summary(site_text, 20)
        cursor.execute("INSERT INTO highlights_site(url,site_text,highlights,submission_time) VALUES ('%s','%s','%s',NOW());" %
                       (site,
                        "\n".join(site_text),
                        "\n".join(highlights)))
        connection.commit()
        return highlights
    return make_error('No website')


@app.route('/upload_text', methods=['POST'])
def upload_text():
    if request.get_json() and 'text' in request.get_json():  # text upload
        text = request.get_json()['text']
        highlights = Summarization.pdf_article_to_summary(text, 4)
        cursor.execute("INSERT INTO highlights_pdf(pdf_text,highlights,submission_time) VALUES ('%s','%s',NOW());" %
                       ("\n".join(text),
                        "\n".join(highlights)))
        connection.commit()
        return json.dumps(highlights)


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' in request.files:  # pdf upload
        file = request.files['file']
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            pdf_text = PDFtoText.pdf_to_text(file)
            highlights = Summarization.pdf_article_to_summary(pdf_text, 4)
            highlights_json = json.dumps(highlights)
            if highlights_json == '':
                return make_error('Invalid file')
            cursor.execute("INSERT INTO highlights_pdf(pdf_text,highlights,submission_time) VALUES (%s,%s,NOW());" %
                           ("'" + "\n".join(pdf_text) + "'",
                            "'" + "\n".join(highlights) + "'"))
            connection.commit()
            return highlights_json
    return make_error('No file uploaded or file not named \'file\'')


def make_error(message):
    resp = jsonify({'message': message})
    resp.status_code = 400
    return resp


if __name__ == '__main__':
    app.run()
