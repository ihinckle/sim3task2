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

    def get_descriptive_stats(self, text):
        sentences = text.split('.')
        words = text.split()
        
        if not words or not sentences:
            return {}

        avg_sentence_length = len(words) / len(sentences)
        unique_words = len(set(words))
        lexical_density = (unique_words / len(words)) * 100

        return {
            "avg_sentence_length": round(avg_sentence_length, 2),
            "lexical_richness": f"{round(lexical_density, 2)}%",
            "total_word_count": len(words),
            "total_sentences": len(sentences)
        }
