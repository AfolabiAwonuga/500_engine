from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords 
from pymongo import MongoClient
from bson.objectid import ObjectId
import string 

def process(doc):
    terms_stemmed = []
    puncs_removed = ''
    ps = PorterStemmer() 
    sw = stopwords.words('english')
    
    for char in doc['description']:
        if char not in string.punctuation:
            puncs_removed += char

    tokenize = word_tokenize(puncs_removed)
    for token in tokenize:
        terms_stemmed.append(ps.stem(token))

    cleaned_terms = []
    for term in terms_stemmed:
        if term not in sw:
            cleaned_terms.append(term)

    return(cleaned_terms)


def create_inverted_index(conn):
    cluster = MongoClient(conn)
    db  = cluster['engine']
    collection = db['data']
    
    termdoc_id = {}
    unsorted_inv_index = {}
    inverted_index = {}
    
    corpus =  collection.find({})
    for doc in corpus:
        for term in process(doc):
            if term not in termdoc_id:
                termdoc_id[term] = []
                termdoc_id[term].append(doc['_id'])
            else:
                termdoc_id[term].append(doc['_id'])

        for key in termdoc_id:
            unsorted_inv_index[key] = [[i, termdoc_id[key].count(i)] for i in set(termdoc_id[key])]

    
    for key in sorted(unsorted_inv_index.keys()):
        inverted_index[key] = unsorted_inv_index[key] 

    return inverted_index
   
   
def store_in_db(conn):
    cluster = MongoClient(conn)
    db  = cluster['engine']
    collection = db['inv_index']
    collection.insert_one(create_inverted_index(conn))


conn = 'mongodb://db:27017'



if __name__ == '__main__':
    store_in_db(conn)
    # print(create_inverted_index(conn))
