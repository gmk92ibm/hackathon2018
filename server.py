#!/usr/bin/env python
import os
import json
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    version='2016-05-20',
    api_key='b9ab4853c2a89aa535738cef3b1e56a2da1f20a7'
)

app = Flask(__name__)

port = int(os.getenv('PORT', 3000))
host = '0.0.0.0'

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static'
configure_uploads(app, photos)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
    image = photos.save(request.files['photo'])

    print image

    with open('./static/' + image, 'rb') as images_file:
        classes = visual_recognition.classify(images_file,classifier_ids=['food_493541751'],threshold=0.0)

    print(json.dumps(classes, indent=2))

    data = {'text': 'asdf'}

    return render_template('image.html', image=image, data=data)

if __name__ == '__main__':
    app.run(host=host, port=port)
