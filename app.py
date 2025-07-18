import requests
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('monitorStatus') == 0:  # Site is down
        try:
            response = requests.get('https://core-east.niftyimages.com/api/health')
            # Save to a file in /tmp (Render’s writable directory)
            with open('/tmp/error_page.html', 'a') as f:
                f.write(f"[{data.get('alertDateTime')}]\n{response.text}\n\n")
        except Exception as e:
            print(f"Error fetching content: {e}")
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)