import numpy as np
from nltk.cluster.util import cosine_distance
import networkx as nx
from nltk.corpus import stopwords


def parse_input(input):
    sentences = []
    for sentence in input:
        onlyAlpha = sentence.replace("[^a-zA-Z]", " ").split(" ")
        removeNewline = [x.replace('\n', '') for x in onlyAlpha]
        sentences.append(removeNewline)
    return sentences


def lower_case(wordlist):
    return list(w.lower() for w in wordlist)


def similarity_matrix(sentences, stop_words):
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


def article_to_summary(input_sentences, num):
    sum_text = []
    sentences = parse_input(input_sentences)

    stop_words = stopwords.words('english')
    matrix = similarity_matrix(sentences, stop_words)  # Building the similarity matrix

    sentence_ranks = nx.from_numpy_array(matrix)  # Ranking
    ranks = nx.pagerank(sentence_ranks)

    sentence_ranks = sorted(((ranks[i], s) for i, s in enumerate(sentences)), reverse=True)  # Rank sorting
    for i in range(num):
        sum_text.append(" ".join(sentence_ranks[i][1]))
    return sum_text

