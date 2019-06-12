import os

import json
from flask import Flask, request, jsonify
from main import process_file


app = Flask(__name__, static_folder='static')
app.config["DEBUG"] = False

SRCDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(SRCDIR, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/parse', methods=['post'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files['file']
            # right now existing cvs contains no ext so we have to add ext here.
            filename = file.filename

            if "." not in filename:
                filename = filename + ".pdf"

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            output = process_file(file_path, debug=True)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return jsonify({'data': json.dumps(output, indent=2, ensure_ascii=False)})
        except Exception as e:
            return jsonify({'error': str(e)})
