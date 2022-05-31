from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html');

@app.route('/v/')
def videoplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer.html', url=request.args.get('url'));

@app.route('/v2/')
def videoplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer2.html', url=request.args.get('url'));

@app.route('/video/')
def video():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer.html', url=request.args.get('url'));

@app.route('/redditvideo/')
def redditplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('hls.html', url=request.args.get('url'));

@app.route('/rvideo/')
def rplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('hls2.html', url=request.args.get('url'));

@app.route('/videoapi/')
def videoapi():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoapi.html', url=request.args.get('url'));


@app.route('/stream1/')
def driveapi():
    if not request.args.get('url'): return redirect('/')
    return render_template('drivestream.html', url=request.args.get('url'), preload=request.args.get('load'));

@app.route('/stream/')
def drivenoneapi():
    if not request.args.get('url'): return redirect('/')
    return render_template('drivestream.html', url=request.args.get('url'), preload='none');

@app.route('/rvid')
def sample():
    if not request.args.get('url'): return redirect('/')
    return render_template('sample.html', url=request.args.get('url'), preload=request.args.get('load'));


@app.route('/test/')
def test():
    a = 'hi'
    return a;


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
