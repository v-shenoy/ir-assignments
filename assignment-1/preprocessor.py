import string
import os
import json
import sys
from collections import defaultdict

import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer


def generate_terms(doc_text):
    table = dict((ord(char), "") for char in string.punctuation)
    doc_text = doc_text.translate(table)

    words = [word for sent in sent_tokenize(doc_text) for word in word_tokenize(sent)]
    stemmer = PorterStemmer()

    terms = [stemmer.stem(word).lower() for word in words]

    return terms


def save_serialized_vector(vocab_json_):
    corpus = os.listdir(os.getcwd())
    corpus_size = len(corpus)

    doc_freq = np.array([val for val in vocab_json.values()])
    inv_doc_freq = np.log(corpus_size/(1+doc_freq))

    for file_name in corpus:
        song_json = None
        with open(file_name, "r") as song_file:
            song_json = json.load(song_file)
       
        print(f"Saving - {file_name}")
        
        term_freq = song_json.get("term_freq", {})
        doc_vec = np.zeros(len(vocab_json.keys()))
        for (idx, key) in enumerate(vocab_json.keys()):
            doc_vec[idx] = term_freq.get(key, 0) 

        doc_vec = np.log(1 + doc_vec)
        song_json["mod"] = doc_vec.dot(doc_vec) ** 0.5
        
        with open(file_name, "w") as output_file:
            json.dump(song_json, output_file, indent = 2, ensure_ascii = False)


if __name__ == "__main__":

    DATASET_DIRECTORY_NAME = "lyrics-dataset"

    if not os.path.isdir(os.path.join(os.getcwd(), DATASET_DIRECTORY_NAME)):
        print("Cannot find dataset directory.")
        sys.exit(1)
    os.chdir(DATASET_DIRECTORY_NAME)

    vocab_json = defaultdict(int)

    for file_name in os.listdir(os.getcwd()):

        song_json = None
        with open(file_name, "r") as song_file:
            song_json = json.load(song_file)
        

        terms = generate_terms(song_json["song_name"])
        terms.extend(generate_terms(song_json["lyrics"]))

        unique_terms = list(set(terms))

        term_freq = dict()
        for term in unique_terms:
            term_freq[term] = terms.count(term)
            vocab_json[term] += 1
        
        song_json["term_freq"] = term_freq
        with open(file_name, "w") as output_file:
            json.dump(song_json, output_file, indent = 2, ensure_ascii = False)


    save_serialized_vector(vocab_json)

    with open("vocab.json", "w") as output_file:
        json.dump(vocab_json, output_file, indent = 2, ensure_ascii = False)
