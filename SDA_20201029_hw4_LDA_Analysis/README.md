[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **SDA_20201029_hw4_LDA_Analysis** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml

Name of Quantlet: 'SDA_20201029_hw4_LDA_Analysis'

Published in: 'SDA_2020_NCTU'

Description: "LDA analysis of the abstracts of a set of scientifique papers to understand main topics that are handled in those papers."

Submitted : 29 October 2020

Input:

Output: heat-map

Keywords: 
- LDA
- Heat-map
- Topic-modelling
- Web Crawling
- Abstract

Author: Bousbiat Hafsa, Andreas Rony Wijaya
```

![Picture1](heatmap_abstract.png)

### IPYNB Code
```ipynb

{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Task_2.ipynb",
      "provenance": [],
      "collapsed_sections": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "metadata": {
        "id": "dhWkyE1MUXvw"
      },
      "source": [
        "pip install feedparser"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "NP7-S1ZQYoPY"
      },
      "source": [
        "import feedparser\n",
        "content = feedparser.parse(\"https://www.ft.com/?edition=international&format=rss\")\n",
        "print(\"\\nTitles-------------------------\\n\")\n",
        "for index, item in enumerate(content.entries):\n",
        "  print(\"{0}.{1}\".format(index, item[\"title\"]))"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "9hHrevqKYt3B"
      },
      "source": [
        "import requests  # take the website source code back to you\n",
        "import urllib  # some useful functions to deal with website URLs\n",
        "from bs4 import BeautifulSoup as soup  # a package to parse website source code\n",
        "import numpy as np  # all the numerical calculation related methods\n",
        "import re  # regular expression package\n",
        "import itertools  # a package to do iteration works\n",
        "import pickle  # a package to save your file temporarily\n",
        "import pandas as pd  # process structured data\n",
        "import os"
      ],
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "FXmJp4X7ZGFv"
      },
      "source": [
        "sub_dir = os.getcwd() + '/DEDA_class2019_SYSU_Abstract_LDA_Crawler/'\n",
        "cwd_dir = sub_dir if os.path.exists(sub_dir) else os.getcwd()  # the path you save your files\n",
        "base_link = 'http://www.wiwi.hu-berlin.de/de/forschung/irtg/results/discussion-papers'  # This link can represent the domain of a series of websites\n",
        "abs_link = 'https://www.wiwi.hu-berlin.de/de/forschung/irtg/results/'\n",
        "# abs_folder = cwd_dir + 'Abstracts/'\n",
        "# os.makedirs(abs_folder, exist_ok=True)\n",
        "\n",
        "\n",
        "request_result = requests.get(base_link, headers={'Connection': 'close'})  # get source code\n",
        "parsed = soup(request_result.content)  # parse source code\n",
        "tr_items = parsed.find_all('tr')\n",
        "info_list = []\n",
        "for item in tr_items:\n",
        "    link_list = item.find_all('td')\n",
        "    try:\n",
        "        paper_title = re.sub(pattern=r'\\s+', repl=' ', string=link_list[1].text.strip())\n",
        "        author = link_list[2].text\n",
        "        date_of_issue = link_list[3].text\n",
        "        abstract_link = link_list[5].find('a')['href']\n",
        "        info_list.append([paper_title, author, date_of_issue, abstract_link])\n",
        "    except Exception as e:\n",
        "        print(e)\n",
        "        print(link_list[5])\n",
        "        continue\n",
        "abstract_all = list()\n",
        "for paper in info_list:\n",
        "    print(paper[0])\n",
        "    try:\n",
        "        paper_abstract_page = requests.get(abs_link + paper[3], headers={'Connection': 'close'})\n",
        "\n",
        "        if paper_abstract_page.status_code == 200:\n",
        "            # if paper[3][-3:] == 'txt':\n",
        "            abstract_parsed = soup(paper_abstract_page.content)\n",
        "            main_part = abstract_parsed.find_all('div', attrs={'id': r'content-core'})[0].text.strip()\n",
        "            # if paper[3][-3:] == 'pdf':\n",
        "            #     abstract_parsed = soup(paper_abstract_page.content)\n",
        "            #     main_part = abstract_parsed.find_all('body')[0].text.strip()\n",
        "\n",
        "            main_part = re.sub(r'.+?[Aa]bstract', 'Abstract', main_part)\n",
        "            main_part = re.sub(r'JEL [Cc]lassification:.*', '', main_part)\n",
        "            main_part = re.sub(r'[A-Za-z][0-9][0-9]?', '', main_part)\n",
        "            main_part = re.sub('[\\r\\n]+', ' ', main_part)\n",
        "\n",
        "            abstract_all.append(main_part + \"\\nSEP\\n\")\n",
        "\n",
        "        else:\n",
        "            raise ConnectionError(f\"Can not access the website. Error Code: {paper_abstract_page.status_code}\")\n",
        "        # with open(abs_folder + f\"{re.sub('[^a-zA-Z0-9 ]', '', paper[0])}.txt\", 'w', encoding='utf-8') as abs_f:\n",
        "        #     abs_f.write(main_part)\n",
        "\n",
        "    except Exception as e:\n",
        "        print(e)\n",
        "        print(paper[3])\n",
        "        continue\n",
        "\n",
        "with open(cwd_dir + 'Abstract_all.txt', 'w') as abs_all_f:\n",
        "    abs_all_f.writelines(abstract_all)"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "WNKsYJ9UaT1D"
      },
      "source": [
        "abstract_all"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "pNpptrmgak6B"
      },
      "source": [
        "import random\n",
        "import os\n",
        "import re\n",
        "import nltk\n",
        "nltk.download('punkt')\n",
        "nltk.download('stopwords')\n",
        "from os import path\n",
        "from nltk.stem import WordNetLemmatizer \n",
        "from nltk.stem.porter import PorterStemmer\n",
        "from nltk.corpus import stopwords\n",
        "from nltk.corpus import stopwords \n",
        "from nltk.stem.wordnet import WordNetLemmatizer\n",
        "import string\n",
        "import gensim\n",
        "from gensim import corpora\n",
        "import matplotlib.pyplot as plt\n",
        "import pandas as pd\n",
        "import numpy as np"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "HTYu2k2Waxbw"
      },
      "source": [
        "doc_l = abstract_all\n",
        "#doc_l.pop()[0]\n",
        "doc_complete = doc_l\n",
        "doc_out = []\n",
        "for l in doc_l:\n",
        "    \n",
        "    cleantextprep = str(l)\n",
        "    \n",
        "    # Regex cleaning\n",
        "    expression = \"[^a-zA-Z ]\" # keep only letters, numbers and whitespace\n",
        "    cleantextCAP = re.sub(expression, ' ', cleantextprep) # apply regex\n",
        "    cleantextCAP = re.sub('\\s+', ' ', cleantextCAP) # apply regex\n",
        "    cleantext = cleantextCAP.lower() # lower case \n",
        "    bound = ''.join(cleantext)\n",
        "    doc_out.append(bound)\n",
        "\n",
        "doc_complete = doc_out\n",
        "stop = set(stopwords.words('english'))\n",
        "stop = stop.union({'result','keywords','study','using','paper','abstract','f','x','e','result','topic','proposed','one'})\n",
        "exclude = set(string.punctuation) \n",
        "lemma = WordNetLemmatizer()\n",
        "import nltk\n",
        "nltk.download('wordnet')\n",
        "def clean(doc):\n",
        "    stop_free = \" \".join([i for i in doc.lower().split() if i not in stop])\n",
        "    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)\n",
        "    normalized = \" \".join(lemma.lemmatize(word) for word in punc_free.split())\n",
        "    return normalized\n",
        "\n",
        "\n",
        "doc_clean = [clean(doc).split() for doc in doc_complete]\n",
        "\n",
        "# Importing Gensim\n",
        "\n",
        "\n",
        "# Creating the term dictionary of our courpus, where every unique term is assigned an index.\n",
        "dictionary = corpora.Dictionary(doc_clean)\n",
        "\n",
        "# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.\n",
        "doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]\n",
        "\n",
        "# Creating the object for LDA model using gensim library\n",
        "Lda = gensim.models.ldamodel.LdaModel\n",
        "\n",
        "# Running and Trainign LDA model on the document term matrix.\n",
        "ldamodel = Lda(doc_term_matrix, num_topics=6, id2word = dictionary, passes=50, random_state = 3154)\n",
        "\n",
        "#print(ldamodel.print_topics(num_topics=6, num_words=5))\n",
        "K=6\n",
        "topicWordProbMat=ldamodel.print_topics(K)\n",
        "\n",
        "columns = ['1','2','3','4','5', '6']\n",
        "df = pd.DataFrame(columns = columns)\n",
        "pd.set_option('display.width', 1000)\n",
        "\n",
        "# 20 need to modify to match the length of vocabulary \n",
        "zz = np.zeros(shape=(100,K))\n",
        "\n",
        "last_number=0\n",
        "DC={}\n",
        "\n",
        "for x in range (100):\n",
        "  data = pd.DataFrame({columns[0]:\"\",\n",
        "                     columns[1]:\"\",\n",
        "                     columns[2]:\"\",\n",
        "                     columns[3]:\"\",\n",
        "                     columns[4]:\"\", \n",
        "                     columns[5]:\"\",                                                                                                 \n",
        "                    },index=[0])\n",
        "  df=df.append(data,ignore_index=True)  \n",
        "\n",
        "for line in topicWordProbMat:\n",
        "    \n",
        "    tp, w = line\n",
        "    probs=w.split(\"+\")\n",
        "    y=0\n",
        "    for pr in probs:\n",
        "               \n",
        "        a=pr.split(\"*\")\n",
        "        df.iloc[y,tp] = a[1]\n",
        "        a[1] = a[1].strip()\n",
        "        if a[1] in DC:\n",
        "           zz[DC[a[1]]][tp]=a[0]\n",
        "        else:\n",
        "           zz[last_number][tp]=a[0]\n",
        "           DC[a[1]]=last_number\n",
        "           last_number=last_number+1\n",
        "        y=y+1\n",
        "\n",
        "print (df)\n",
        "print (zz)"
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "X6vDaPncbMY5"
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "irwUy6S1bVpn",
        "outputId": "64655ada-50c0-4bf9-a434-068daff7fcd5",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 1000
        }
      },
      "source": [
        "zz=np.resize(zz,(len(DC.keys()),zz.shape[1]))\n",
        "plt.figure(figsize=(80,25))\n",
        "for val, key in enumerate(DC.keys()):\n",
        "        plt.text(-2.5, val + 0.5, key,\n",
        "                 horizontalalignment='center',\n",
        "                 verticalalignment='center'\n",
        "                 )\n",
        "#plt.imshow(zz, cmap='hot', interpolation='nearest')\n",
        "plt.imshow(zz, cmap='rainbow', interpolation='nearest')\n",
        "#plt.show()\n",
        "plt.yticks([])\n",
        "# plt.title(\"heatmap xmas song\")\n",
        "plt.savefig(\"heatmap_abstract.png\", transparent = True, dpi=400)"
      ],
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "image/png": "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\n",
            "text/plain": [
              "<Figure size 5760x1800 with 1 Axes>"
            ]
          },
          "metadata": {
            "tags": [],
            "needs_background": "light"
          }
        }
      ]
    }
  ]
}
```

automatically created on 2020-11-18

### PYTHON Code
```python

# -*- coding: utf-8 -*-
"""Task_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X9TzY0fFcSgqnebo7RtVluYhtkAXopW2
"""

pip install feedparser

import feedparser
content = feedparser.parse("https://www.ft.com/?edition=international&format=rss")
print("\nTitles-------------------------\n")
for index, item in enumerate(content.entries):
  print("{0}.{1}".format(index, item["title"]))

import requests  # take the website source code back to you
import urllib  # some useful functions to deal with website URLs
from bs4 import BeautifulSoup as soup  # a package to parse website source code
import numpy as np  # all the numerical calculation related methods
import re  # regular expression package
import itertools  # a package to do iteration works
import pickle  # a package to save your file temporarily
import pandas as pd  # process structured data
import os

sub_dir = os.getcwd() + '/DEDA_class2019_SYSU_Abstract_LDA_Crawler/'
cwd_dir = sub_dir if os.path.exists(sub_dir) else os.getcwd()  # the path you save your files
base_link = 'http://www.wiwi.hu-berlin.de/de/forschung/irtg/results/discussion-papers'  # This link can represent the domain of a series of websites
abs_link = 'https://www.wiwi.hu-berlin.de/de/forschung/irtg/results/'
# abs_folder = cwd_dir + 'Abstracts/'
# os.makedirs(abs_folder, exist_ok=True)


request_result = requests.get(base_link, headers={'Connection': 'close'})  # get source code
parsed = soup(request_result.content)  # parse source code
tr_items = parsed.find_all('tr')
info_list = []
for item in tr_items:
    link_list = item.find_all('td')
    try:
        paper_title = re.sub(pattern=r'\s+', repl=' ', string=link_list[1].text.strip())
        author = link_list[2].text
        date_of_issue = link_list[3].text
        abstract_link = link_list[5].find('a')['href']
        info_list.append([paper_title, author, date_of_issue, abstract_link])
    except Exception as e:
        print(e)
        print(link_list[5])
        continue
abstract_all = list()
for paper in info_list:
    print(paper[0])
    try:
        paper_abstract_page = requests.get(abs_link + paper[3], headers={'Connection': 'close'})

        if paper_abstract_page.status_code == 200:
            # if paper[3][-3:] == 'txt':
            abstract_parsed = soup(paper_abstract_page.content)
            main_part = abstract_parsed.find_all('div', attrs={'id': r'content-core'})[0].text.strip()
            # if paper[3][-3:] == 'pdf':
            #     abstract_parsed = soup(paper_abstract_page.content)
            #     main_part = abstract_parsed.find_all('body')[0].text.strip()

            main_part = re.sub(r'.+?[Aa]bstract', 'Abstract', main_part)
            main_part = re.sub(r'JEL [Cc]lassification:.*', '', main_part)
            main_part = re.sub(r'[A-Za-z][0-9][0-9]?', '', main_part)
            main_part = re.sub('[\r\n]+', ' ', main_part)

            abstract_all.append(main_part + "\nSEP\n")

        else:
            raise ConnectionError(f"Can not access the website. Error Code: {paper_abstract_page.status_code}")
        # with open(abs_folder + f"{re.sub('[^a-zA-Z0-9 ]', '', paper[0])}.txt", 'w', encoding='utf-8') as abs_f:
        #     abs_f.write(main_part)

    except Exception as e:
        print(e)
        print(paper[3])
        continue

with open(cwd_dir + 'Abstract_all.txt', 'w') as abs_all_f:
    abs_all_f.writelines(abstract_all)

abstract_all

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

doc_l = abstract_all
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
ldamodel = Lda(doc_term_matrix, num_topics=6, id2word = dictionary, passes=50, random_state = 3154)

#print(ldamodel.print_topics(num_topics=6, num_words=5))
K=6
topicWordProbMat=ldamodel.print_topics(K)

columns = ['1','2','3','4','5', '6']
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
```

automatically created on 2020-11-18