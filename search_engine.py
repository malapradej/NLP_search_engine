#!/bin/python
''' A search engine that loads a json file and creates an indexed from
which fast searches could be done.
Requires the json, nltk and sklearn libraries for python.
Make sure that the following nltk libraries are downloaded:
    punkt
    wordnet
Run the script using:
    $ python search_engine.py
You will be required to enter the search terms including field specific
operators. To close the script use Ctrl-C.
'''

import json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

prod_json = json.load(open('products.json', 'r'))

descrs = []
titles = []
merchs = []
alltxt = []

# class for the tokenizer and lemmatizer
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

# tfidf vectorizer object
vect = TfidfVectorizer(tokenizer=LemmaTokenizer(), stop_words='english') 

# read json mappings to lists per key 
for l in prod_json:
    desc = l['description']
    titl = l['title']
    merc = l['merchant']
    merchs.append(merc)
    titles.append(titl)
    descrs.append(desc)

# fit vectorizer and return tfidf matrices
tfidf_mat_d = vect.fit_transform(descrs)
feature_names_d = vect.get_feature_names()
tfidf_mat_t = vect.fit_transform(titles)
feature_names_t = vect.get_feature_names()
tfidf_mat_m = vect.fit_transform(merchs)
feature_names_m = vect.get_feature_names()

# infinite loop for multiple queries
while True:
    # get user search terms or close
    try:
        print('Separate terms with spaces. Precede fields with either')
        print('d= t= or m= if searching only in description, title or')
        print('merchant fields. Ctrl-C to close.')
        search_txt = input('search text: ')
    except KeyboardInterrupt:
        break
    search_txt = search_txt.lower().split()
    wnl = WordNetLemmatizer()
    
    records = []
    tfidf = []
    sort = []
    
    # search terms in lists, includes exceptions
    for txt in search_txt:
        if txt[:2] == 'd=':
            try:
                i = feature_names_d.index(wnl.lemmatize(txt[2:]))
            except ValueError:
                print('Search text not in description field.')
            else:
                records.append(tfidf_mat_d.getcol(i).tocoo().row)
                d = tfidf_mat_d.getcol(i).tocoo().data
                tfidf.append(d)
        elif txt[:2] == 't=':
            try:
                i = feature_names_t.index(wnl.lemmatize(txt[2:]))
            except ValueError:
                print('Search text not in title field.')
            else:
                records.append(tfidf_mat_t.getcol(i).tocoo().row)
                d = tfidf_mat_t.getcol(i).tocoo().data
                tfidf.append(d)
        elif txt[:2] == 'm=':
            try:
                i = feature_names_m.index(wnl.lemmatize(txt[2:]))
            except ValueError: 
                print('Search text not in merchant field.')
            else:
                records.append(tfidf_mat_m.getcol(i).tocoo().row)
                d = tfidf_mat_m.getcol(i).tocoo().data
                tfidf.append(d)
        else:
            try:
                i = feature_names_d.index(wnl.lemmatize(txt))
            except ValueError:
                print('Search text not in description field.')
            else:
                records.append(tfidf_mat_d.getcol(i).tocoo().row)
                d = tfidf_mat_d.getcol(i).tocoo().data
                tfidf.append(d)
            try:
                i = feature_names_t.index(wnl.lemmatize(txt))
            except ValueError:
                print('Search text not in title field.')
            else:
                records.append(tfidf_mat_t.getcol(i).tocoo().row)
                d = tfidf_mat_t.getcol(i).tocoo().data
                tfidf.append(d) 
            try:
                i = feature_names_m.index(wnl.lemmatize(txt))
            except ValueError:
                print('Search text not in merchant field.')
            else:
                records.append(tfidf_mat_m.getcol(i).tocoo().row) 
                d = tfidf_mat_m.getcol(i).tocoo().data
                tfidf.append(d)
    
    # flatten lists
    records = [item for arr in records for item in arr]
    tfidf = [item for arr in tfidf for item in arr]
    
    # if duplicate records sum duplicates tfidf
    records_dups = []
    tfidf_dups = []
    tally = []
    
    for i in range(len(records)):
        if i in tally:
            continue
        records_dups.append(records[i])
        tfidf_dups.append(tfidf[i])
        for j in range(i+1, len(records)):
            if records[i] == records[j]:
                tfidf_dups[-1] += tfidf[j]
                tally.append(j)
    
    # sort tfidf values in descending order
    sort = sorted(range(len(tfidf_dups)), key=tfidf_dups.__getitem__, reverse=True)
    
    search_docs = []
    search_index = []
    for s in sort:
        r = records_dups[s]
        search_docs.append(prod_json[r])
        search_index.append(r)
    
    print('Search result:')
    print(search_docs) 
