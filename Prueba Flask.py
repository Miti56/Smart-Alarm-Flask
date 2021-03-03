
from flask import Flask
from flask import request



app = Flask(__name__)

@app.route('/')

def hello():
    alarm = request.args.get("alarm")
    if alarm:
        print(alarm)
    return '<form action="/"method="get"> \
        <input type="datetime-local" name="alarm"> \
        <input type="submit"></form>'

if __name__ == "__main__":
    app.run()

