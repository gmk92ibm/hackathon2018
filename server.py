#!/usr/bin/env python
import os
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

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
    data = {'text': 'asdf'}
    return render_template('image.html', image=image, data=data)

if __name__ == '__main__':
    app.run(host=host, port=port)
