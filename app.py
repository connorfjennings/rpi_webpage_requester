from flask import Flask, request, render_template, redirect
import threading
from utils import extract_info_from_search, extract_info_from_url, play_video_url

app = Flask(__name__)
videoQ = []
Qsema = threading.Semaphore(value=0)
playSema = threading.Semaphore(value=0)
Qlock = threading.Lock()
videoDic = {}
player = None
currentlyPlaying = "None :("
def runQueue():
	while True:
		global player, currentlyPlaying
		Qsema.acquire()
		Qlock.acquire()
		videoQ.sort(reverse = True, key = lambda x: x["votes"])
		info_dict = videoQ.pop(0)
		currentlyPlaying = info_dict["title"]
		videoDic.pop(info_dict["id"])
		url = info_dict.get("webpage_url", None)
		player = play_video_url(url, videoEndedCallback)
		Qlock.release()
		playSema.acquire()

def videoEndedCallback(arg1):
	playSema.release()


@app.route('/')
def index():
	return redirect("/success")

@app.route('/success')
def success():
	global currentlyPlaying
	passQ = videoQ.copy()
	videoQ.sort(reverse = True, key = lambda x: x["votes"])
	if len(videoQ) == 0:
		currentlyPlaying = "None :("
	return render_template("success.html", length = len(passQ), videos = passQ, playing = currentlyPlaying)


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
	return redirect("/success")


@app.route('/vote/<id>')
def vote(id):
	vote = request.args['vote']
	info_dict = videoDic[id]
	if (vote == "upvote"):
		info_dict["votes"] += 1
	elif (vote == "downvote"):
		info_dict["votes"] -= 1
	return redirect("/success")

@app.route('/close')
def close():
	global player
	player.quit()
	return redirect("/success")



if __name__ == '__main__':
	qThread = threading.Thread(target=runQueue, daemon=True)
	qThread.start()
	app.run(debug=False, host='0.0.0.0')