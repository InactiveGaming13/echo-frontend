from flask import Flask, Blueprint, render_template, request, redirect, url_for as urlFor
from flask_socketio import SocketIO, emit

# Create the Flask app
app = Flask(__name__)

# Configure the Flask app
app.config["SECRET_KEY"] = "UBF)*(VB)PD:CV^6gf8evf8y0o6asfCG*VO*)^vfc"

# Create the Flask blueprints
static: Blueprint = Blueprint("static", __name__, static_folder="static", static_url_path="/static")

# Register the Flask blueprints
app.register_blueprint(static, url_prefix="/static")

# Create the SocketIO object
socketio = SocketIO(app)


def renderTemplate(template: str, error: str | None = None, success: str | None = None) -> str:
    if success and error:
        raise ValueError("Cannot have both an error and a success message!")
    return render_template(template, error=error, success=success, account={
        "username": "User",
        "email": "test@provider.com",
        "userID": "1234567890"})


# Define the route for the index page
@app.route("/")
def index():
    return renderTemplate("index.html")


# Start the Flask app
if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8050, debug=True, allow_unsafe_werkzeug=True)
