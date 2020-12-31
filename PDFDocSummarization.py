#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from nltk.cluster.util import cosine_distance
import networkx as nx
from nltk.corpus import stopwords


# In[2]:


def read_file(file_name):
    input_file = open(file_name, "r", encoding='utf-8').readlines()
    sentences = []
    for sentence in input_file:
        onlyAlpha = sentence.replace("[^a-zA-Z]", " ").split(" ")
        removeNewline = [x.replace('\n', '') for x in onlyAlpha]
        sentences.append(removeNewline)
    return sentences


# In[3]:


def lower_case(wordlist):
    return list(w.lower() for w in wordlist)


# In[4]:


def similarityMatrix(sentences, stop_words):
    matrix = np.zeros((len(sentences), len(sentences)))

    # Comparing the sentences
    for sent1_loc in range(len(sentences)):
        for sent2_loc in range(len(sentences)):
            if sent1_loc == sent2_loc:
                continue
            first = sentences[sent1_loc]
            second = sentences[sent2_loc]
            first = lower_case(first)
            second = lower_case(second)

            word_concat = list(set(first + second))

            enc1 = [0] * len(word_concat)
            enc2 = [0] * len(word_concat)

            for w in first:
                if w not in stop_words:
                    enc1[word_concat.index(w)] += 1

            for w in second:
                if w not in stop_words:
                    enc2[word_concat.index(w)] += 1

            matrix[sent1_loc][sent2_loc] = 1 - cosine_distance(enc1, enc2)

    return matrix


# In[5]:


def article_to_summary(input_file, num):
    sum_text = []
    sentences = read_file(input_file)

    stop_words = stopwords.words('english')
    matrix = similarityMatrix(sentences, stop_words)  # Building the similarity matrix

    sentence_ranks = nx.from_numpy_array(matrix)  # Ranking
    ranks = nx.pagerank(sentence_ranks)

    sentence_ranks = sorted(((ranks[i], s) for i, s in enumerate(sentences)), reverse=True)  # Rank sorting
    for i in range(num):
        sum_text.append(" ".join(sentence_ranks[i][1]))
    print("\033[1m" + "Highlights" + "\033[0m")
    for sen in sum_text:
        print("\u2022 " + sen.lstrip())
    sum_text = " ".join(sum_text)
    # print("Summarized Text: \n",sum_text)
    return sum_text


# In[6]:


file2_output = article_to_summary("input-file.txt", 4)

# In[7]:


# count = 2
# for i in range(2,6):
#     fileName1 = "inputFile"+str(count)+".txt"
#     fileName2 = "outputFile"+str(count)+".txt"
#     count = count + 1
#     file_output = article_to_summary(fileName1,3)
#     print(file_output)
#     np.savetxt(fileName2, [file_output] , fmt='%s')

