from flask import Flask, request, render_template
import threading
from .utils import extract_info_from_search, extract_info_from_url
app = Flask(__name__)
videoQ = []
Qsema = threading.Semaphore(value=0)
def runQueue():
	while True:
		Qsema.acquire()
		info_dict = videoQ.pop(0)
		url = info_dict.get("url", None)
		


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/open')
def open():
	website = request.args['website']
	radio = request.args['method']
	if (radio == "Video"):
		info = extract_info_from_url(website)
		videoQ.append(info)
		Qsema.release()
	elif (radio == "Lucky"):
		info = extract_info_from_search(website)
		videoQ.append(info)
		Qsema.release()
	return render_template("index.html")

@app.route('/vote')
def vote():
	website = request.args['website']
	return render_template("index.html")

if __name__ == '__main__':
	qThread = threading.Thread(target=runQueue, daemon=True)
	qThread.start()
	app.run(debug=False, host='0.0.0.0')