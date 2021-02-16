from flask import Flask, request, jsonify
from flask.helpers import send_file
from io import BytesIO

from .strategies import BetweenPageStrategy
from .core import add_blank_page

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__, static_url_path='', static_folder='static')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/between-page/<nb_pages>/<alpha>', methods=['POST'])
def add_blank_page_server(nb_pages, alpha):
    try:
        nb_pages = int(nb_pages)
        alpha = float(alpha)
    except ValueError:
        return jsonify({'error': 'invalid type for parameters /page-between/<nb_pages:int>/<alpha:float>'})
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'})
    [input_file, *_] = request.files.getlist('file')
    input_file = BytesIO(input_file.read())
    output_file = BytesIO()
    try:
        add_blank_page(input_file, BetweenPageStrategy(
            nb_pages, alpha), output_file)
    except Exception as e:
        return jsonify({'error': str(e)})
    output_file.seek(0)
    return send_file(output_file, 'application/pdf')
