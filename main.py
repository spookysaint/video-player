from flask import Flask, render_template, request, redirect
import base64, requests, random
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html');

@app.route('/v/')
def videoplayer():
    url = request.args.get('url')
    return render_template('videoplayer.html', url=url.replace('vid.r', random.choice(['vid.r', 'vid2.r'])), loading='metadata');
@app.route('/reload')
def reload():
   r = requests.get("https://gitlab.com/rishabh-modi2/public/-/raw/main/video-player.py")
   open('main.py', 'wb').write(r.content)
   return "reloaded"

@app.route('/v2/')
def vidaplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer2.html', url=request.args.get('url'), load=request.args.get('load'));

@app.route('/video/')
def video():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer.html', url=request.args.get('url'));

@app.route('/audio/')
def audio():
    if not request.args.get('url'): return redirect('/')
    return render_template('audioplayer.html', url=request.args.get('url'), load=request.args.get('load'));

@app.route('/redditvideo/')
def redditplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('hls.html', url=request.args.get('url'));

@app.route('/rvideo/')
def rplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('hls2.html', url=request.args.get('url'));

@app.route('/stream/')
def driveapi():
    if not request.args.get('url'): return redirect('/')
    base64_string = request.args.get('url')
    base64_bytes = base64_string.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return render_template('drivestream.html', url=f"{sample_string}", loading=request.args.get('loading'));




if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
