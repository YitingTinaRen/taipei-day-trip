from app import login_manager
from liff.db.models import User


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(line_user_id=user_id).first()
    return user if user else None
