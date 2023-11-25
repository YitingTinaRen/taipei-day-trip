import config
from flask import Blueprint, render_template, request, abort
from liff.utility import validate_line_signature


liff_blueprint = Blueprint(
    "liff", __name__, template_folder="templates", static_folder="static"
)
# the template_folder, static_folder argument,
# either an absolute path or relative to the blueprint’s location


@liff_blueprint.route("/index")
@validate_line_signature
def index():
    return render_template("main.html", liff_id=config.LIFF_ID)
