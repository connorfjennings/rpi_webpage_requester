from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/open')
def open():
	website = request.args['website']
	radio = request.args['method']
	return render_template("index.html")

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')