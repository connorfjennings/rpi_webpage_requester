from flask import Flask, request, render_template

app = Flask(__name__)
videoQ = []


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/open')
def open():
	website = request.args['website']
	radio = request.args['method']
	if (radio == "video"):
		videoQ.append(website)
	return render_template("index.html")

@app.route('/remove')
def remove():
	website = request.args[website]
	videoQ.remove(website)
	return render_template("index.html")
	
if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')