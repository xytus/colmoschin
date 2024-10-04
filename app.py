from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Welcome to Our Simple Flask Web Application</h1>
    <p>This is a basic Flask web application used for demonstrating CI/CD and security testing.</p>
    <p>Created by: Col Moschin</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
