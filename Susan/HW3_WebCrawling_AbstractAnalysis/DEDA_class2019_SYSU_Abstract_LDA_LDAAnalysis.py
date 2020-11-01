
import random
import os
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from os import path
from nltk.stem import WordNetLemmatizer 
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


d = os.getcwd()

text_pre = open('Abstract_all.txt', encoding = "utf8").read()


doc_l = str.split(text_pre, sep = 'SEP')
#doc_l.pop()[0]

doc_complete = doc_l

doc_out = []
for l in doc_l:
    
    cleantextprep = str(l)
    
    # Regex cleaning
    expression = "[^a-zA-Z ]" # keep only letters, numbers and whitespace
    cleantextCAP = re.sub(expression, ' ', cleantextprep) # apply regex
    cleantextCAP = re.sub('\s+', ' ', cleantextCAP) # apply regex
    cleantext = cleantextCAP.lower() # lower case 
    bound = ''.join(cleantext)
    doc_out.append(bound)

doc_complete = doc_out



stop = set(stopwords.words('english'))
stop = stop.union({'result','keywords','study','using','paper','abstract','f','x','e','result','topic','proposed','one'})
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
import nltk
nltk.download('wordnet')
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


doc_clean = [clean(doc).split() for doc in doc_complete]    


# Importing Gensim


# Creating the term dictionary of our courpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]


# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=7, id2word = dictionary, passes=50, random_state = 3154)

#print(ldamodel.print_topics(num_topics=3, num_words=5))
K=7
topicWordProbMat=ldamodel.print_topics(K)




columns = ['1','2','3','4','5', '6', '7']
df = pd.DataFrame(columns = columns)
pd.set_option('display.width', 1000)

# 20 need to modify to match the length of vocabulary 
zz = np.zeros(shape=(100,K))

last_number=0
DC={}

for x in range (100):
  data = pd.DataFrame({columns[0]:"",
                     columns[1]:"",
                     columns[2]:"",
                     columns[3]:"",
                     columns[4]:"",                                                                                                    
                     columns[5]:"",                                                                                                    
                     columns[6]:"",                                                                                                    
                    },index=[0])
  df=df.append(data,ignore_index=True)  

for line in topicWordProbMat:
    
    tp, w = line
    probs=w.split("+")
    y=0
    for pr in probs:
               
        a=pr.split("*")
        df.iloc[y,tp] = a[1]
        a[1] = a[1].strip()
        if a[1] in DC:
           zz[DC[a[1]]][tp]=a[0]
        else:
           zz[last_number][tp]=a[0]
           DC[a[1]]=last_number
           last_number=last_number+1
        y=y+1

print (df)
print (zz)




zz=np.resize(zz,(len(DC.keys()),zz.shape[1]))
plt.figure(figsize=(80,25))
for val, key in enumerate(DC.keys()):
        plt.text(-2.5, val + 0.5, key,
                 horizontalalignment='center',
                 verticalalignment='center'
                 )

#plt.imshow(zz, cmap='hot', interpolation='nearest')
plt.imshow(zz, cmap='rainbow', interpolation='nearest')
#plt.show()
plt.yticks([])
# plt.title("heatmap xmas song")
plt.savefig("heatmap_abstract.png", transparent = True, dpi=400)

