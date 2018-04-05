#!/usr/bin/env python

from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=3000)
