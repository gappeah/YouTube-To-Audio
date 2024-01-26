from flask import Flask, render_template, request, send_file
import pytube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = pytube.YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    out_file = audio.download()
    base, ext = os.path.splitext(out_file)
    new_file = base + '.m4a'
    os.rename(out_file, new_file)
    return send_file(new_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
