from flask import Flask, render_template

from threading import Thread

app =Flask(__name__)

@app.route('/')
def index():
  return "TTSOYQIZ ishlamoqda 1000 -portda"

def run():
  app.run(host='0.0.0.0',port=1000)

def keep_alive():
  t=Thread(target=run)
  t.start()
