from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords 
from pymongo import MongoClient
from bson.objectid import ObjectId
import streamlit as st 
import numpy as np
import string 

def find(conn):
    st.title('500 Engine')
    search = st.text_input('Search')
    
    cluster = MongoClient(conn)
    db  = cluster['engine']
    corpus = db['data']
    inverted_index = db['inv_index']
    
    sw = stopwords.words('english')
    ps = PorterStemmer()
    puncs_removed = ''
    temp_query = []
    processed_query = []

    tfidf_scores = []
    score_dict = {}
    score_doc_list = []
    doc_id = []
    total_docs = corpus.count_documents({})

    #       PRE PROCESSING   
    tab1, tab2 = st.tabs(["Sweetwater", "Thomann"])  
    if search:
        for char in search:
            if char not in string.punctuation:
                puncs_removed += char 

        for token in word_tokenize(puncs_removed):
            temp_query.append(ps.stem(token))

        for term in temp_query:
            if term not in sw:
                processed_query.append(term)


        for word in processed_query:
            try:
                word_in_invindex = inverted_index.find_one({},{word:1})[word]
            except:
                continue
            
            total_docs_word_appears = len(word_in_invindex)

            for docid_tf in word_in_invindex:  
                tf = np.log(1 + docid_tf[1])
                idf = np.log(total_docs / total_docs_word_appears)
                tf_idf  = round((tf * idf),2) 
                tfidf_doc = [tf_idf, docid_tf[0]]
                tfidf_scores.append(tfidf_doc)         

        for score in tfidf_scores:
            if score[1] not in score_dict:
                score_dict[score[1]] = []
                score_dict[score[1]].append(score[0])
            else:
                score_dict[score[1]].append(score[0])

        for val in score_dict:
            score_dict[val] = round(sum(score_dict[val]), 2)  

        for key, value in score_dict.items():
            temp = [value, key]
            score_doc_list.append(temp)
            score_doc_list.sort(reverse = True)

        for i in score_doc_list:
            doc_id.append(i[1])     

        
        for doc in doc_id:
            # st.write(doc)
            data = corpus.find_one({'_id':doc},{'_id':0})
            
            if data['store'] == 'Sweetwater':
                with tab1:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(' ')

                    with col2:
                        st.image(data['image'], width = 100)
                   
                    with col3:
                        st.write(' ')    
                    
                    with st.expander('info', expanded = True):
                        st.write('Title:', data['title'])
                        st.write('Price:', data['price'])
                        st.write('Url:', data['url'])
                        try:
                            st.write('Description:', data['description']) 
                        except:
                            pass    
                          
                        # st.write('Category:', data['category'])  
            else:
                with tab2:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(' ')

                    with col2:
                        st.image(data['image'])
                   
                    with col3:
                        st.write(' ')

                    with st.expander('info', expanded = True):
                        st.write('Title:', data['title'])
                        st.write('Price:', data['price'])
                        st.write('Url:', data['url'])
                        try:
                            st.write('Description:', data['description']) 
                        except:
                            pass  
                        


    else:
        for data in corpus.find({},{'_id':0}):
            if data['store'] == 'Sweetwater':
                with tab1:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(' ')

                    with col2:
                        st.image(data['image'], width = 100)
                   
                    with col3:
                        st.write(' ')    
                    
                    with st.expander('info', expanded = True):
                        st.write('Title:', data['title'])
                        st.write('Price:', data['price'])
                        st.write('Url:', data['url'])
                        try:
                            st.write('Description:', data['description']) 
                        except:
                            pass   
                          
                        # st.write('Category:', data['category'])  
            else:
                with tab2:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(' ')

                    with col2:
                        st.image(data['image'])
                   
                    with col3:
                        st.write(' ')

                    with st.expander('info', expanded = True):
                        st.write('Title:', data['title'])
                        st.write('Price:', data['price'])
                        st.write('Url:', data['url'])
                        try:
                            st.write('Description:', data['description']) 
                        except:
                            pass  


conn = 'mongodb://db:27017'
if __name__ == '__main__':
	find(conn)
