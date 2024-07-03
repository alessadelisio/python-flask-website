from flask import Flask, render_template
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.applications import Starlette

from src.routes.health import router as health_router
from src.routes.upload import router as upload_router

app = Flask(__name__)

app.register_blueprint(health_router)
app.register_blueprint(upload_router)


@app.route("/")
def index():  # noqa: D103
    return render_template("index.html")


@app.route("/compare")
def compare():  # noqa: D103
    return render_template("pages/compare.html")


asgi_app = Starlette()
asgi_app.mount("/", WSGIMiddleware(app))

if __name__ == "__main__":
    app.run(debug=True)
