import io

import ebooklib
import joblib
from bs4 import BeautifulSoup
from ebooklib import epub
from flask import Blueprint, render_template, request, jsonify

from db.models import SosPrediction, db, SosError
from utils import TextProcessor

book_bp = Blueprint('book_bp', __name__)

model = joblib.load('./model/ai-text-detector-model.pkl')
text_processor = TextProcessor()

@book_bp.route('/')
def home_page():  # put application's code here
	return render_template('predict.html.j2')

@book_bp.route('/about')
def about_page():
	return render_template('about.html.j2')

@book_bp.route('/monitor')
def monitor_page():
	return render_template('monitor.html.j2')


@book_bp.route('/predict-book', methods=['POST'])
def predict_book():
	uploaded_file = request.files.get('book')

	if uploaded_file is None:
		return 'Uploaded file error'

	if not uploaded_file.filename.lower().endswith('.epub'):
		db.session.add(SosError(error=f"Invalid file extension for {uploaded_file.filename}"))
		db.session.commit()
		return jsonify({"success": False, "error": "Invalid file extension. Please upload an EPUB file."}), 400

	book_file = io.BytesIO(uploaded_file.read())
	book = epub.read_epub(book_file)

	if book is None:
		db.session.add(SosError(error=f"There was an issue reading the epub file {uploaded_file.filename}"))
		db.session.commit()
		return jsonify({"success": False, "error": "There was an issue reading the epub file."}), 400

	title = book.get_metadata('DC', 'title')[0][0]
	author = book.get_metadata('DC', 'creator')[0][0]

	exists = db.session.query(SosPrediction).filter_by(title=title, author=author).first()

	if exists:
		return jsonify({
			"success": True,
			"result": exists.result,
			"title": exists.title,
			"author": exists.author,
			"exists": True
		})

	full_text = get_book_text(book)
	cleaned_text = text_processor.full_clean(full_text)

	result = model.predict([cleaned_text])[0]

	descriptive_stats = text_processor.get_descriptive_stats(full_text)

	db.session.add(SosPrediction(title=title,
								 author=author,
								 result=result))
	db.session.commit()

	return jsonify({
		"success": True,
		"result": result,
		"analysis": descriptive_stats,
		"title": title,
		"author": author
	})


def get_book_text(book):
	full_text = []

	for item in book.get_items():
		if item.get_type() == ebooklib.ITEM_DOCUMENT:
			soup = BeautifulSoup(item.get_content(), 'html.parser')

			for element in soup(['script', 'style', 'image', 'svg', 'header', 'footer']):
				element.decompose()

			text = soup.get_text(separator=' ', strip=True)
			full_text.append(text)

	return ' '.join(full_text)
