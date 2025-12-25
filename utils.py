import string
import nltk
from nltk.corpus import stopwords

class TextProcessor:
    def __init__(self):
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')

        self.stop_words = set(stopwords.words('english'))

    def remove_tags(self, text):
        tags = ['\n', '\'']
        for tag in tags:
            text = text.replace(tag, '')
        return text

    def remove_punc(self, text):
        return ''.join([x for x in text if x not in string.punctuation])

    def remove_stopwords(self, text):
        words = nltk.word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        return ' '.join(filtered_words)

    def full_clean(self, text):
        text = self.remove_tags(text)
        text = self.remove_punc(text)
        text = self.remove_stopwords(text)
        return text
