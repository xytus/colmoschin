from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to the Simple Flask App</h1><p>This application was created by Col Moschin.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
