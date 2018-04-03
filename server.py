#! /usr/bin/env python
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

port = int(os.getenv('PORT', 3000))
host = '0.0.0.0'

@app.route('/')
def root():
	return render_template('index.html')

@app.route('/get', methods=['GET'])
def get():
	print request.args['text']
	return jsonify({'data': request.args['text']})

@app.route('/post', methods=['POST'])
def post():
	print request.form['text']
	return jsonify({'data': request.form['text']})

if __name__ == '__main__':
	app.run(host=host, port=port)
