from flask import Blueprint, render_template
import config
from flask import request
from liff.db.command import db


liff_blueprint = Blueprint(
    "liff", __name__, template_folder="templates", static_folder="static"
)
# the template_folder, static_folder argument,
# either an absolute path or relative to the blueprint’s location


@liff_blueprint.route("/index")
def index():
    return render_template("main.html", liff_id=config.LIFF_ID)


@liff_blueprint.route("/call-off")
def off():
    return render_template("off.html", liff_id=config.LIFF_ID)


@liff_blueprint.route("/summary")
def summary():
    sql = """
    select 	id, 
		CASE 
		WHEN source_id = 1 THEN '請假'
		WHEN source_id = 2 THEN '換班'
		WHEN source_id = 3 THEN '加班'
		WHEN source_id = 4 THEN '家長請假'
		ELSE NULL
		END AS source_id,
        CASE 
        WHEN source_id = 1 and source_type = 1 THEN '年假'
        WHEN source_id = 1 and source_type = 1 THEN '病假'
        WHEN source_id = 1 and source_type = 1 THEN '事假'
        ELSE NULL
        END AS source_type,
		start_date, end_date, off_hours, 
        IF(note is null, '', note) AS note
    from nanny_attandence
    where is_valid is True;
    """
    rows = db().checkAllData(sql)
    return render_template("summary.html", liff_id=config.LIFF_ID, rows=rows)
