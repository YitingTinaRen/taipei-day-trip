from flask import Blueprint

liff_app_api = Blueprint("liff_app_api", __name__)


@liff_app_api.route("/api/google/update-sheet", methods=["POST"])
def update_sheet():
    pass
