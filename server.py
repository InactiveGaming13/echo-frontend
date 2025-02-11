from flask import Flask, Blueprint, render_template as renderTemplate, request, redirect, url_for as urlFor
# from flask_socketio import SocketIO, emit
from flask_sse import sse

# Create the Flask app
app = Flask(__name__)

# Configure the Flask app
app.config["SECRET_KEY"] = "UBF)*(VB)PD:CV^6gf8evf8y0o6asfCG*VO*)^vfc"
app.config["REDIS_URL"] = "redis://localhost"

# Create the Flask blueprints
static: Blueprint = Blueprint("static", __name__, static_folder="static", static_url_path="/static")

# Register the Flask blueprints
app.register_blueprint(sse, url_prefix="/stream")
app.register_blueprint(static, url_prefix="/static")

# Create the SocketIO object
# socketio = SocketIO(app)


# Define the route for the index page
@app.route("/")
def index():
    return renderTemplate("index.html")


# Define the route for the stream page
@app.route("/sendstream")
def send_stream():
    sse.publish({"message": "Hello, world!"}, type="message")
    return "Message sent!"


# Start the Flask app
if __name__ == "__main__":
    # socketio.run(app, host="127.0.0.1", port=8050, allow_unsafe_werkzeug=True)
    app.run(host="127.0.0.1", port=8050, debug=True)
