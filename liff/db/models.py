from app import db


class NannyAttandence(db.Model):
    __tablename__ = "nanny_attandence"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.Integer, nullable=False)
    source_type = db.Column(db.String(20), nullable=True)
    is_valid = db.Column(db.Boolean, nullable=False, default=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    off_hours = db.Column(db.Float, nullable=False, default=0)
    note = db.Column(db.String(256), nullable=True)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    last_modifier = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    last_modified_date = db.Column(db.DateTime, nullable=False)

    # Explicitly specify foreign keys for the relationships
    associated_creator = db.relationship(
        "User", foreign_keys=[creator], backref="nanny_attandence_creator", lazy=True
    )
    associated_last_modifier = db.relationship(
        "User",
        foreign_keys=[last_modifier],
        backref="nanny_attandence_last_modifier",
        lazy=True,
    )

    def __repr__(self):
        return "<NannyAttandence %r>" % self.id


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    line_user_id = db.Column(db.String(255), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    last_modified_date = db.Column(db.DateTime, nullable=False)
    # Define backref for nanny_attandence_creator relationship
    # Define backref for the relationship with NannyAttandence
    nanny_attandence_creator = db.relationship(
        "NannyAttandence",
        foreign_keys=[NannyAttandence.creator],
        backref="creator_user",
        lazy=True,
    )

    nanny_attandence_last_modifier = db.relationship(
        "NannyAttandence",
        foreign_keys=[NannyAttandence.last_modifier],
        backref="last_modifier_user",
        lazy=True,
    )

    def __repr__(self):
        return "<User %r>" % self.id
