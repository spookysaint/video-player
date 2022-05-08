from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html');

@app.route('/v/')
def videoplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer.html', url=request.args.get('url'));

@app.route('/video/')
def video():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer.html', url=request.args.get('url'));

@app.route('/redditvideo/')
def redditplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('hls.html', hls=request.args.get('url'));


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
