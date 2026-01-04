from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SosPrediction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	author = db.Column(db.String(100), nullable=False)
	result = db.Column(db.Float, nullable=False)

class SosError(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	error = db.Column(db.String(1000), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())