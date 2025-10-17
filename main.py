from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/transcript', methods=['POST'])
def get_transcript():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL required'}), 400
        
        pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, url)
        
        if not match:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        video_id = match.group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([entry['text'] for entry in transcript])
        
        return jsonify({
            'success': True,
            'video_id': video_id,
            'transcript': full_text,
            'segments': len(transcript)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'YouTube Transcript API',
        'usage': 'POST /transcript with {"url": "youtube_url"}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
