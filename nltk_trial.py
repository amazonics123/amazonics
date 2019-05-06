import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentence = "At eight o'clock on Thursday morning, Arthur didn't feel very good."
tokens = nltk.word_tokenize(sentence)
print(tokens)
tagged = nltk.pos_tag(tokens)
print(tagged)
entities = nltk.chunk.ne_chunk(tagged)
print(entities)

def analyze_sentences(sentences):
    '''
    Takes in a LIST of sentences and spits out some cool stuff.
    '''
    sid = SentimentIntensityAnalyzer()
    for sentence in sentences:
        print(sentence)
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
        print()
