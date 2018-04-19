# NLP_search_engine
A Natural Language Processing product search engine based on a TFIDF ranking. Includes stopwords, lemmatization and tokenization. 
Reads a json file of products. Field specific searches can be done using operators. 

Clone into a repository on your computer. 
To run the script use the command line:

    $ python search_engine.py
  
 You will be asked to type the search terms including field specific operators:
 
 
 eg. If you want to search for a term only on the title field precede the search term by `t=` for example `t=biography`. 
 You can search mutliple words. Words not preceded by a field specific operator will be searched in all fields.
 The search will return results ranked by TFIDF weighting with the highest ranked products at the top. 
