from textrank import TextRank
import sys
import os
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if (request.method == 'POST'):
    	payload = request.get_json()
    	input_text = payload["text"]
    	t = TextRank(input_text)
    	t.analyze(50)
    	t.generate_cloud().to_file("temp.png")
    	return send_file("temp.png", mimetype='image/png')

if __name__ == '__main__':
	input_file = open(sys.argv[1])
	t = TextRank(input_file.read(), iterations=100)
	t.analyze(30)
	t.generate_cloud()
	# app.config['TEMPLATES_AUTO_RELOAD'] = True
	# app.run(host='0.0.0.0', port=8080)