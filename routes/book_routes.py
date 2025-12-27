import io

import ebooklib
import joblib
from bs4 import BeautifulSoup
from ebooklib import epub
from flask import Blueprint, render_template, request

from db.models import Prediction, db
from utils import TextProcessor

book_bp = Blueprint('book_bp', __name__)

model = joblib.load('./model/ai-text-detector-model.pkl')
text_processor = TextProcessor()

@book_bp.route('/')
def home_page():  # put application's code here
	return render_template('index.html.j2')


@book_bp.route('/predict-book', methods=['POST'])
def predict_book():
	uploaded_file = request.files.get('book')

	if uploaded_file is None:
		return 'Uploaded file error'

	book_file = io.BytesIO(uploaded_file.read())
	book = epub.read_epub(book_file)

	if book is None:
		return 'Epub file error'

	full_text = get_book_text(book)
	cleaned_text = text_processor.full_clean(full_text)

	result = model.predict([cleaned_text])[0]

	db.session.add(Prediction(title=request.form.get('title'), author=request.form.get('author'), result=result))
	db.session.commit()

	return render_template('prediction-response.html.j2', result=result)


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
