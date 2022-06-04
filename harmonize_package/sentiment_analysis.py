from harmonize_package import app
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from spacy import displacy




class SentimentAnalyzer:

    def __init__(self, entry_body):
        self.snlp = spacy.load('en_core_web_sm')
        self.entry_text_to_analyze = entry_body
        self.entry_analyzer = SentimentIntensityAnalyzer()
        self.polarity_scores = self.entry_analyzer.polarity_scores(self.entry_text_to_analyze)


    def get_polarity_scores(self):
        return self.polarity_scores

    def get_polarity_score_percentages(self):
        polarity_percent_value_list = []
        neg_percent = round(self.polarity_scores['neg'] * 100, 4)
        polarity_percent_value_list.append(neg_percent)
        neu_percent = round(self.polarity_scores['neu'] * 100, 4)
        polarity_percent_value_list.append(neu_percent)
        pos_percent = round(self.polarity_scores['pos'] * 100, 4)
        polarity_percent_value_list.append(pos_percent)
        compound_percent = round(self.polarity_scores['compound'] * 100, 4)
        polarity_percent_value_list.append(compound_percent)

        return polarity_percent_value_list

    def get_snlp(self):
        return self.snlp

    def process_text_w_snlp(self):
        #### SpaCy logic for NER ####
        # create a document (for python 3 all strings are unicode by default, no need to cast)
        entry_document = self.snlp(self.entry_text_to_analyze)

        return entry_document




