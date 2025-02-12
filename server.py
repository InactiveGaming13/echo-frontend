from flask import Flask, Blueprint, render_template, request, redirect, url_for as urlFor, Response, make_response
from flask_socketio import SocketIO

# Create the Flask app
app: Flask = Flask(__name__)

# Configure the Flask app
app.config["SECRET_KEY"] = "UBF)*(VB)PD:CV^6gf8evf8y0o6asfCG*VO*)^vfc"

# Create the Flask blueprints
static: Blueprint = Blueprint("static", __name__, static_folder="static", static_url_path="/static")

# Register the Flask blueprints
app.register_blueprint(static, url_prefix="/static")

# Create the SocketIO object
socketio: SocketIO = SocketIO(app)


def renderTemplate(template: str, error: str | None = None, success: str | None = None, logged: bool = False) -> str:
    # Check if both an error and a success message exist
    if success and error:
        raise ValueError("Cannot have both an error and a success message!")

    # Check if the client is not logged in
    if not logged:
        return render_template(template, error=error, success=success)

    # Render the template with the account information if the client is logged in
    return render_template(template, error=error, success=success, account={
        "username": "User",
        "email": "test@provider.com",
        "userID": "1234567890"})


# Define the route for the index page
@app.route("/")
def index() -> str | Response:
    # Check if a success cookie exists
    if request.cookies.get("success"):
        success: str = request.cookies.get("success")
        response: Response = make_response(renderTemplate("index.html", success=success))
        response.set_cookie("success", "", expires=0)
        return response

    # Check if an error cookie exists
    if request.cookies.get("error"):
        error: str = request.cookies.get("error")
        response: Response = make_response(renderTemplate("index.html", error=error))
        response.set_cookie("error", "", expires=0)
        return response

    # Check if the client is logged in
    if request.cookies.get("userId"):
        return renderTemplate("index.html", logged=True)

    # Render the index page if no cookies exist
    return renderTemplate("index.html")


# Define the route for the login page
@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    # Check if the client is posting data
    if request.method == "POST":
        return renderTemplate("login.html", error="Server error: Could not log in!")

    # Render the login page if the client is not posting data
    return renderTemplate("login.html")


# Define the route for the register page
@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    # Check if the client is posting data
    if request.method == "POST":
        return renderTemplate("register.html", error="Server error: Could not create account!")

    # Render the register page if the client is not posting data
    return renderTemplate("register.html")


# Define the route for the account page
@app.route("/account", methods=["GET", "POST"])
def account() -> str:
    # Check if the client is posting data
    if request.method == "POST":
        return renderTemplate("account.html", error="Server error: Could not update account!")

    # Render the account page if the client is not posting
    return renderTemplate("account.html")


# Define the route for the logout page
@app.route("/logout")
def logout() -> Response:
    # Create a response with a success cookie to inform the client that they have logged out
    response: Response = redirect(urlFor("index"))
    response.set_cookie("success", "Successfully logged out!")
    return response


# Define the route for the app page
@app.route("/app")
def appPage() -> str | Response:
    # Check if the client isn't logged in
    if not request.cookies.get("userId"):
        response: Response = redirect(urlFor("index"))
        response.set_cookie("error", "You must be logged in to access the app!")
        return response

    # Render the app page if the client is logged in
    return renderTemplate("app.html", logged=True)


# Define the route for the 404 page
@app.errorhandler(404)
def notFound(e: Exception) -> str:
    print(e)
    return renderTemplate("404.html")


# Start the Flask app
if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8050, debug=True, allow_unsafe_werkzeug=True)
