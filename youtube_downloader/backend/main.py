from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube, Playlist
import io
import zipfile

app = Flask(__name__)
CORS(app) 

@app.route('/download-content', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    type = data.get('type')

    if not url or not type:
        return {'error': 'No URL or TYPE provided'}, 400
    
    try:
        buffer = io.BytesIO()

        if 'playlist' in url:
            playlist = Playlist(url)

            with zipfile.ZipFile(buffer, 'w') as zipf:
                for video in playlist.videos:
                    if type == 'MP4':
                        content = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                        filename = f"{video.title}.mp4"
                    else:
                        content = video.streams.filter(only_audio=True).first()
                        filename = f"{video.title}.mp3"

                    video_buffer = io.BytesIO()
                    content.stream_to_buffer(video_buffer)
                    video_buffer.seek(0)
                    
                    zipf.writestr(filename, video_buffer.read())

            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name='playlist.zip', mimetype='application/zip')
        else:
            yt = YouTube(url)

            if type == 'MP4':
                content = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            else:
                content = yt.streams.filter(only_audio=True).first()

            content.stream_to_buffer(buffer)
            buffer.seek(0)

            if type == 'MP4':
                return send_file(buffer, as_attachment=True, download_name='video.mp4', mimetype='video/mp4')
            else:
                return send_file(buffer, as_attachment=True, download_name='audio.mp3', mimetype='audio/mpeg')


    # try:
    #     yt = YouTube(url)

    #     if type == 'MP4':
    #         content = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    #     else:
    #         content = yt.streams.filter(only_audio=True).first()

    #     buffer = io.BytesIO()
    #     content.stream_to_buffer(buffer)
    #     buffer.seek(0)

    #     if type == 'MP4':
    #         return send_file(buffer, as_attachment=True, download_name='video.mp4', mimetype='video/mp4')
    #     else:
    #         return send_file(buffer, as_attachment=True, download_name='audio.mp3', mimetype='audio/mpeg')
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)