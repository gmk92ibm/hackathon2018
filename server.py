#!/usr/bin/env python
import os
import json
import requests
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

    with open('./static/' + image, 'rb') as images_file:
        results = visual_recognition.classify(images_file,classifier_ids=['food_493541751'],threshold=0.0)

    classes = results['images'][0]['classifiers'][0]['classes']

    max_score = 0

    max_class = ''

    for x in classes:
        if x['score'] > max_score:
            max_score = x['score']
            max_class = x['class']

    print max_class

    app_id  = 'a7965555'
    app_key = '23c96db4a0d2f7928414cd96f5cdc8c4'

    params = {'q': max_class, 'app_id': app_id, 'app_key': app_key}

    r = requests.get('https://api.edamam.com/search', params=params)

    data = {'recipes': []}

    for x in r.json()['hits']:
        print x['recipe']['label']
        print x['recipe']['url']
        tmp = {}
        tmp['title'] = x['recipe']['label']
        tmp['url'] = x['recipe']['url']
        data['recipes'].append(tmp)

    print data

    return render_template('image.html', image=image, data=data)

if __name__ == '__main__':
    app.run(host=host, port=port)
