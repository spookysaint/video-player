from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
import io,uuid, base64, os, pathlib, requests
from flask import Flask, render_template, request, jsonify, Response, send_file, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)
   

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive_service = build('drive', 'v3', http=creds.authorize(Http()))

def uploadFile(file_name, mime):
    file_metadata = {
    'name': file_name,
    'mimeType': mime,
    "parents": ['1wnUgeiT-_sd_3mXqA37g4hrWnTX5R7ny']}
    media = MediaFileUpload(file_name,
                            mimetype=mime,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
    return file.get('id')

image = {'.jpg', '.jpeg', '.png'}
video = {'.mp4', '.mkv'}
audio = {'.mp3', '.ogg'}
def file(filetype, f):
    filename = str(uuid.uuid4()) + filetype
    if filetype == 'nigga':
        print('nigga')
    
    elif filetype in video:
        f.save(filename)
        sample_string = uploadFile(filename, 'video/mp4')
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        print('file Video')
        os.remove(filename)
        resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer2.rishabh.ml/video-ui/?url=" + f"{base64_string}" + "&loading=none' height='360' width=100% allowfullscreen=True></iframe></div>"
        return resp

    elif filetype in image:
        f.save(filename)
        uploadFile(filename, 'image/jpg')
        os.remove(filename)
        resp = "<img src='https://backend.rishabh.ml/0:/" + filename + "'>"
        return resp

    elif filetype in audio:
        f.save(filename)
        uploadFile(filename, 'audio/mpeg')
        os.remove(filename)
        resp = "<div class='embed-responsive embed-responsive-16by9'><iframe src='https://videoplayer.rishabh.ml/audio/?url=https://backend.rishabh.ml/0:/" + filename + "&load=none' height='360' width=100% allowfullscreen=True></iframe></div>"
        return resp
    with open('logs.txt', 'a+') as fa:
        fa.write(request.headers.get('X-Forwarded-For', request.remote_addr) + ' uploaded ' + filename + '\n')
        fa.close()
folder = 'uploaded_files'
@app.route('/upload')
def upload_file():
   return render_template('upload.html')
    
@app.route('/loggs')
def loggg():
   return send_file('logs.txt', mimetype='text/plain')

@app.route('/reloadupload')
def reload():
   r = requests.get("https://gitlab.com/rishabh-modi2/public/-/raw/main/combine.py")
   open('app.py', 'wb').write(r.content)
   return "reloaded"

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_fileto():
   if request.method == 'POST':
      f = request.files['file']
      if '.png' or '.jpg' or '.jpeg' or '.mp4' or '.mkv' or '.mp3' or '.pdf' in f.filename:
        if '.png' in f.filename:
            res = file('.png', f)
            return render_template('response.html', embedcode=res)
        if '.jpg' in f.filename:
            res = file('.jpg', f)
            return render_template('response.html', embedcode=res)        
        if '.jpeg' in f.filename:
            res = file('.jpeg', f)
            return render_template('response.html', embedcode=res)
        
        if '.mkv' in f.filename:
            res = file('.mkv', f)
            return render_template('response.html', embedcode=res)
        
        if '.mp4' in f.filename:
            res = file('.mp4', f)
            return render_template('response.html', embedcode=res)

        if '.mp3' in f.filename:
            res = file('.mp3', f)
            return render_template('response.html', embedcode=res)
        
        if '.pdf' in f.filename:
            filename = f.filename
            f.save(filename)
            uploadFile(filename)
            os.remove(filename)
            resp = "<iframe src=http://docs.google.com/gview?url=https://backend.rishabh.ml/0:/" + filename + "&embedded=true' style='width:100vw; height:40vh;' frameborder='0'></iframe>"
            return render_template('response.html', embedcode=res)


@app.route('/')
def index():
    return render_template('index.html');

@app.route('/v/')
def videoplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer.html', url=request.args.get('url'));
@app.route('/reload')
def reload():
   r = requests.get("https://gitlab.com/rishabh-modi2/public/-/raw/main/video-player.py")
   open('app.py', 'wb').write(r.content)
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
