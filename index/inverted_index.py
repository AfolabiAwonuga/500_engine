from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords 
from pymongo import MongoClient
from bson.objectid import ObjectId
import string 


def process(
         doc: str
) -> list:
    """
    Processes text data by removing punctuation, stemming terms, and removing stopwords.

    Args:
        doc (str): Data to be processed.

    Returns:
        list: A list of cleaned and stemmed terms.

    """ 
    terms_stemmed = []
    puncs_removed = ''
    ps = PorterStemmer() 
    sw = stopwords.words('english')
    
    # Remove punctuation from the document
    for char in doc['description']:
        if char not in string.punctuation:
            puncs_removed += char

    # Tokenize the cleaned text
    tokenize = word_tokenize(puncs_removed)

    # Stem and filter out stopwords
    for token in tokenize:
        terms_stemmed.append(ps.stem(token))
    cleaned_terms = []
    for term in terms_stemmed:
        if term not in sw:
            cleaned_terms.append(term)

    return(cleaned_terms)


def create_inverted_index(
        conn
) -> dict:
    """
    Creates an inverted index for the documents in a MongoDB collection.

    Args:
        conn (str): Connection string for MongoDB.

    Returns:
        dict: An inverted index where keys are terms and values are lists of [document_id, term_frequency] pairs.

    """
    # Establish connection to MongoDB
    cluster = MongoClient(conn)
    db  = cluster['engine']
    collection = db['data']
    
    termdoc_id = {}
    unsorted_inv_index = {}
    inverted_index = {}
    
    # Fetch all documents from the collection
    corpus =  collection.find({})
    for doc in corpus:
        # Process each document to get cleaned terms
        for term in process(doc):
            if term not in termdoc_id:
                termdoc_id[term] = []
                termdoc_id[term].append(doc['_id'])
            else:
                termdoc_id[term].append(doc['_id'])

        # Create unsorted inverted index
        for key in termdoc_id:
            unsorted_inv_index[key] = [[i, termdoc_id[key].count(i)] for i in set(termdoc_id[key])]

    # Sort the inverted index by term
    for key in sorted(unsorted_inv_index.keys()):
        inverted_index[key] = unsorted_inv_index[key] 

    return inverted_index
   
   
def store_in_db(
        conn
) -> None:
    """
    Stores the inverted index in a MongoDB collection.

    Args:
        conn (str): Connection string for MongoDB.

    Returns:
        None

    """
    # Establish connection to MongoDB
    cluster = MongoClient(conn)
    db  = cluster['engine']
    collection = db['inv_index']

    # Insert the inverted index into the collection
    collection.insert_one(create_inverted_index(conn))


if __name__ == '__main__':
    conn = 'mongodb://db:27017'
    store_in_db(conn)

