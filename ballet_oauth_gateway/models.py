from ballet_oauth_gateway import db


class Auth(db.Model):
    __tablename__ = 'auths'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String(40), nullable=False)
    code = db.Column(db.String(20), nullable=False)
