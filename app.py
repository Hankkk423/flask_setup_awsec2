from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire application

@app.route('/')
@cross_origin()  # Enable CORS for this specific route
def hello_world():
	return 'Hello World!'

if __name__ == "__main__":
	app.run()