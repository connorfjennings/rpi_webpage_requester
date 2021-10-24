from flask import Flask, request, render_template
import threading
app = Flask(__name__)
videoQ = []
Qsema = threading.Semaphore(value=0)
def runQueue():
	while True:
		Qsema.acquire()
		print("HERE IT IS: " + videoQ.pop(0))


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/open')
def open():
	website = request.args['website']
	radio = request.args['method']
	if (radio == "Video"):
		videoQ.append(website)
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