from flask import Flask
from threading import Thread


app = Flask('')

@app.route('/')
def home():
    return '''
<head>
  <title>RAGA bot Status</title>
</head>
<body>
  <h1 style="color: green">STATUS : ONLINE :)</h1>
  <p>Rate limit has been reset :)</p>
</body>'''

def run():
  app.run(host='0.0.0.0',port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()