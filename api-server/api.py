from flask import Flask, jsonify, make_response, request, abort, redirect, send_file
import logging
import base64
import uuid
import os
import sys

import emotion_gender_processor as eg_processor

app = Flask(__name__)


@app.route('/model_app/face_classification/detect', methods=['POST'])
def upload():
    try:
        image = request.files.get('image')
        if not image:
            return make_response('Please provide \'image\' for detect.\n', 400)
        filename = str(uuid.uuid4()) + '-' + image.filename
        eg_processor.process_image(image.read(), filename, app.config.get('model_path'))
        return make_response(jsonify(convert_data(filename)), 200)
    except Exception as err:
        logging.error('An error has occurred whilst processing the file: "{0}"'.format(err))
        abort(400)


def convert_data(filename):
    result = {"type": "img"}
    with open("./result/" + '%s' % filename, "rb") as img_file:
        img_data = base64.b64encode(img_file.read())
    result['data'] = ("data:image/jpg;base64,%s" % img_data.decode())
    os.remove("./result/" + '%s' % filename)
    return result

@app.errorhandler(400)
def bad_request(erro):
    return make_response(jsonify({'error': 'We cannot process the file sent in the request.'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource no found.'}), 404)

if __name__ == '__main__':
    app.config['model_path'] = sys.argv[1]
    app.run(debug=True, host='0.0.0.0', port=80)
