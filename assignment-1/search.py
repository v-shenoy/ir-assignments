import string
import math
import os
import json
import sys
import heapq

import numpy as np

import preprocessor


def partial_cos_sim(query_vec, doc_vec, doc_mod):

    query_mod = query_vec.dot(query_vec) ** 0.5
    dot_product = query_vec.dot(doc_vec)
    
    denom = query_mod * doc_mod
    if denom == 0:
        return 0
    
    return dot_product/denom


if __name__ == "__main__":

    DATASET_DIRECTORY_NAME = "lyrics-dataset"

    if not os.path.isdir(os.path.join(os.getcwd(), DATASET_DIRECTORY_NAME)):
        print("Cannot find dataset directory.")
        sys.exit(1)
    os.chdir(DATASET_DIRECTORY_NAME)

    corpus = os.listdir(os.getcwd())
    corpus_size = len(corpus) - 1

    vocab_json = None
    with open("vocab.json", "r") as vocab_file:
            vocab_json = json.load(vocab_file)

    query = input("Enter song lyrics to search - ")
    terms = preprocessor.generate_terms(query)
    unique_terms = list(set(terms))


    query_vec = np.array([terms.count(term) for term in unique_terms])
    query_vec = np.log(1 + query_vec)
    
    doc_freq = np.array([vocab_json.get(term, 0) for term in unique_terms])
    inv_doc_freq = np.log(corpus_size/(1+doc_freq))

    query_vec = query_vec * inv_doc_freq
    
    top_results = []

    for (idx, file_name) in enumerate(corpus):
        if file_name == "vocab.json":
            continue
        
        song_json = None
        with open(file_name, "r") as song_file:
            song_json = json.load(song_file)
        
        term_freq = song_json.get("term_freq", {})
        doc_vec = np.array([term_freq.get(term, 0) for term in unique_terms])
        doc_vec = np.log(1 + doc_vec)
        doc_vec = doc_vec * inv_doc_freq
        doc_mod = song_json.get("mod", 0)
        sim = partial_cos_sim(query_vec, doc_vec, doc_mod)

        heapq.heappush(top_results, (sim, idx))
        if len(top_results) > 10:
            heapq.heappop(top_results)
        

    top_results = sorted(top_results, reverse = True)
    for result in top_results:
        sim = result[0]
        file_name = corpus[result[1]]
        if sim > 0:
            song_json = None
            with open(file_name, "r") as song_file:
                song_json = json.load(song_file)
            print("\nSong name - {}, Similarity = {}".format(song_json["song_name"], round(100*sim, 2)))
            print("Artist - {}".format(song_json["artist_name"]))
            print("Album - {}".format(song_json["album"]))
            print("Produced by - {}".format(song_json["produced_by"]))
            print("Release date - {}".format(song_json["date"]))
            print("URL for lyrics - {}".format(song_json["song_link"]), end = "\n\n")