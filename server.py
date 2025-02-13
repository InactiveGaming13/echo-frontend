from flask import Flask, Blueprint, render_template, request, redirect, url_for as urlFor, Response, make_response
from flask.templating import Template
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
socketio: SocketIO = SocketIO(app, cors_allowed_origins="*")


def renderTemplate(template: str | Template | list[str | Template], error: str | None = None, success: str | None = None, userId: str = "") -> str:
    # Check if both an error and a success message exist
    if success and error:
        raise ValueError("Cannot have both an error and a success message!")

    # Check if the client is not logged in
    if userId == "" or not userId:
        return render_template(template, error=error, success=success)

    # Render the template with the account information if the client is logged in
    return render_template(
        template,
        error=error,
        success=success,
        account={
            "username": "User",
            "email": "test@provider.com",
            "userID": "1234567890"
        }
    )


def renderError(errorCode: str | int = 500,
                errorTitle: str = "500 - Internal Server Error",
                errorDetails: str = "It seems our server has encountered and error!"
                ) -> str:
    return render_template(
        "errorPage.html",
        errorCode=errorCode,
        errorTitle=errorTitle,
        errorDetails=errorDetails
    )


def handleRedirectCookie(_request: request, _redirect: str | None = None, setting: bool = False, redirectUri: str | None = None) -> Response | None:
    """
    Handles the redirect cookie.

    Args:
         _request (request): The HTTP request object.
         _redirect (str): The location the client should go to during the request (Use endpoint function name).
         setting (bool): True if setting the cookie else, False if redirecting.
         redirectUri (str | None): The redirectUri that the cookie should be set to (Use endpoint function name).
    """
    if not setting and not _request:
        raise ValueError("_request is required.")

    if setting and not _redirect:
        raise ValueError("_redirect is required.")

    if setting and not redirectUri:
        raise ValueError("Cannot set redirect cookie without redirectUri.")

    if setting:
        response: Response = redirect(urlFor(_redirect))
        response.set_cookie("redirectUri", redirectUri)
        return response

    redirectUri = _request.cookies.get("redirectUri")
    if redirectUri:
        response: Response = redirect(urlFor(redirectUri))
        response.set_cookie("redirectUri", "", expires=0)
        return response

    return None


# Define the route for the index page
@app.route("/", methods=["GET"])
def index() -> str | Response:
    success: str = request.cookies.get("success")
    error: str = request.cookies.get("success")
    userId: str = request.cookies.get("userId")

    # Check if a success cookie exists
    if success:
        response: Response = make_response(renderTemplate("index.html", success=success, userId=userId))
        response.set_cookie("success", "", expires=0)
        return response

    # Check if an error cookie exists
    if error:
        response: Response = make_response(renderTemplate("index.html", error=error, userId=userId))
        response.set_cookie("error", "", expires=0)
        return response

    # Render the index page if no cookies exist
    return renderTemplate("index.html", userId=userId)


# Define the route for the login page
@app.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    # Check if the client is posting data
    if request.method == "POST":
        redirectUri: Response = handleRedirectCookie(request)
        if redirectUri:
            redirectUri.set_cookie("userId", "1234567890")
            return redirectUri
        response: Response = redirect(urlFor("index"))
        response.set_cookie("success", "Successfully logged in")
        response.set_cookie("userId", "1234567890")
        return response

    if request.cookies.get("userId"):
        return renderTemplate("index.html", error="You are already logged in!", userId=request.cookies.get("userId"))

    response: Response = make_response(render_template("login.html", error=request.cookies.get("error")))
    response.set_cookie("error", "", expires=0)
    return response


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
def account() -> str | Response:
    # Check if the client is posting data
    if request.method == "POST":
        return renderTemplate("account.html", error="Server error: Could not update account!")

    userId: str = request.cookies.get("userId")

    if not userId:
        response: Response = handleRedirectCookie(request, "login", True, "account")
        response.set_cookie("error", "You must be logged in to edit an account!")
        return response

    # Render the account page if the client is not posting
    return renderTemplate("account.html", userId=userId)


# Define the route for the logout page
@app.route("/logout")
def logout() -> Response:
    # Create a response with a success cookie to inform the client that they have logged out
    response: Response = redirect(urlFor("index"))
    if request.cookies.get("userId"):
        response.set_cookie("userId", "", expires=0)
        response.set_cookie("success", "Successfully logged out!")
    return response


# Define the route for the app page
@app.route("/app")
def appPage() -> str | Response:
    userId: str = request.cookies.get("userId")
    # Check if the client isn't logged in
    if not userId:
        response: Response = handleRedirectCookie(request, "login", True, "appPage")
        response.set_cookie("error", "You must be logged in to access the app!")
        return response

    # Render the app page if the client is logged in
    return renderTemplate("app.html", userId=userId)


@app.route("/ben", methods=["POST"])
def ben() -> str:
    return renderTemplate("index.html")


@app.route("/teapot", methods=["GET"])
def teapot() -> str:
    return renderError(
        errorCode=418,
        errorTitle="418 - I'm A Teapot",
        errorDetails="How the hell did you get to this error? You tried to brew coffee with a teapot! You fool!"
    )


@app.route("/coffee", methods=["GET"])
def coffee() -> Response:
    return redirect("https://en.wikipedia.org/wiki/Stimulant")


@app.errorhandler(401)
def unauthorized(e: Exception) -> Response:
    return redirect(urlFor("index"))


@app.errorhandler(403)
def forbidden(e: Exception) -> str:
    return renderError(
        errorCode=403,
        errorTitle="403 - Forbidden",
        errorDetails="You are not authorized to access this resource."
    )


# Define the route for the 404 page
@app.errorhandler(404)
def notFound(e: Exception) -> str:
    return renderError(
        errorCode=404,
        errorTitle="404 - Not Found",
        errorDetails="Uh oh! It seems you have stumbled upon an unknown URL!"
    )


@app.errorhandler(405)
def methodNotAllowed(e: Exception) -> str:
    return renderError(
        errorCode=405,
        errorTitle="405 - Method Not Allowed",
        errorDetails="It seems like you have stumbled upon a disallowed method!"
    )


@app.errorhandler(418)
def imATeapot(e: Exception) -> str:
    return renderError(
        errorCode=418,
        errorTitle="418 - I'm A Teapot",
        errorDetails="How the hell did you get to this error? You tried to brew coffee with a teapot! You fool!"
    )


# Start the Flask app (DEVELOPMENT ONLY)
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8050, debug=True, allow_unsafe_werkzeug=True)
