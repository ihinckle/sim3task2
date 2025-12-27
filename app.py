from flask import Flask

from db.models import db
from routes.book_routes import book_bp

app = Flask(__name__)
app.register_blueprint(book_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
	db.create_all()

if __name__ == '__main__':
	app.run()
