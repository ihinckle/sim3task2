from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prediction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	author = db.Column(db.String(100), nullable=False)
	result = db.Column(db.Float, nullable=False)
