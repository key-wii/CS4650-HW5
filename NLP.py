import newsapi
import spacy
from newsapi import NewsApiClient
import pickle
import pandas as pd
from collections import Counter
from string import punctuation
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nlp_eng = spacy.load('en_core_web_lg')
newsapi = NewsApiClient (api_key='02f0ae732bcb4f2db1d77ef4288f237e')

def data(x):
    temp = newsapi.get_everything(q='coronavirus', language='en',
        from_param='2022-02-27', to='2022-03-27',
        sort_by='relevancy', page=x)
    return temp

dados = []
articles = list(map(data, range(1, 6)))
print(articles)

filename = 'articlesCOVID.pckl'
pickle.dump(articles, open(filename, 'wb'))

for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        description = x['description']
        content = x['content']
        dados.append({'title': title, 'desc': description, 'content': content})
df = pd.DataFrame(dados)
df = df.dropna()
df.head()

def get_keywords_eng(text):
    result = []
    pos_tag = ['PROPN', 'VERB', 'NOUN']
    doc = nlp_eng(text)
    for token in doc:
        if (token.text in nlp_eng.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return result

results = []
for content in df.content.values:
    results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])
df['keywords'] = results

text = str(results)
text_file = open('result.txt', 'w')
text_file.write(text)

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="black").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()