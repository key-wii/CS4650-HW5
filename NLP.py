import newsapi
import spacy
from newsapi import NewsApiClient
import pickle
import pandas as pd

nlp_eng = spacy.load('en_core_web_lg')
newsapi = NewsApiClient (api_key='02f0ae732bcb4f2db1d77ef4288f237e')

data = newsapi.get_everything(q='coronavirus', language='en',
    from_param='2022-02-27', to='2022-03-27', sort_by='relevancy', page_size = 100)

print("total result: " + str(data['totalResults']))

dados = {}
titles = []
dates = []
descriptions = []
articles = data['articles']

filename = 'articlesCOVID.pckl'
pickle.dump(articles, open(filename, 'wb'))
text_file = open('result.txt')

for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        description = x['description']
        content = x['content']
        dados.append({'title':titles[0], 'date':dates[0], 'desc':descriptions[0], 'content':content})
        text_file.write("information from the API call")
df = pd.DataFrame(dados)
df = df.dropna()
df.head()

