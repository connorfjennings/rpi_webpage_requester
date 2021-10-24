from flask import Flask, request, render_template
import threading
from utils import extract_info_from_search, extract_info_from_url, play_video_url

app = Flask(__name__)
videoQ = []
Qsema = threading.Semaphore(value=0)
playSema = threading.Semaphore(value=0)
Qlock = threading.Lock()
videoDic = {}
player = None
def runQueue():
	while True:
		Qsema.acquire()
		Qlock.acquire()
		videoQ.sort(reverse = True, key = lambda x, y: x["votes"] > y["votes"])
		info_dict = videoQ.pop(0)
		videoDic.pop(info_dict["id"])
		url = info_dict.get("url", None)
		player = play_video_url(url, videoEndedCallback)
		Qlock.release()
		playSema.acquire()

def videoEndedCallback(arg1, arg2):
	playSema.release()


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/open')
def open():
	website = request.args['website']
	radio = request.args['method']
	if (radio == "Video"):
		info_dict = extract_info_from_url(website)
		info_dict["votes"] = 1
		videoDic[info_dict["id"]] = info_dict
		Qlock.acquire()
		videoQ.append(info_dict)
		Qlock.release()
		Qsema.release()
	elif (radio == "Lucky"):
		info_dict = extract_info_from_search(website)
		info_dict["votes"] = 1
		videoDic[info_dict["id"]] = info_dict
		Qlock.acquire()
		videoQ.append(info_dict)
		Qlock.release()
		Qsema.release()
	return render_template("success.html")

@app.route('/vote')
def vote():
	website = request.args['website']
	return render_template("index.html")

@app.route('/close')
def close():
	player.quit()
	return render_template("index.html")



if __name__ == '__main__':
	qThread = threading.Thread(target=runQueue, daemon=True)
	qThread.start()
	app.run(debug=False, host='0.0.0.0')