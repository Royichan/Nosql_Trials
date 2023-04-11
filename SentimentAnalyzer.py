import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def analyze_reviews(comments):
    if comments != None:
        analyzer = SentimentIntensityAnalyzer()
        comment_scores = {"pos":0.0, "neg":0.0, "neu":0.0}
        for comment in comments:
            scores = analyzer.polarity_scores(comment)
            del scores["compound"]
            sorted_scores = sorted(scores.items(), key=lambda x: x[1])
            high = max(scores.values())
            for key in scores.keys():
                if high == scores[key]:
                    comment_scores[key] += scores[key]
        return comment_scores
    else:
        return None