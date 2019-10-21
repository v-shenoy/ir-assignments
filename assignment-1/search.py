''' 
Module responsibly for performing the search using the query,
and the cosine similarity measure. '''

import string
import math
import os
import json
import sys
import heapq

import numpy as np

import preprocessor

json_list = None
vocab_json = None


def partial_cos_sim(query_vec, doc_vec, doc_mod):
    ''' Calculates the cosine similarity between two vectors. 
    Parameters : 
        query_vec - numpy weight vector for query
        doc_vec - numpy weight vector for document
        doc_mod - precomputed document weight vector modulus
    '''

    query_mod = query_vec.dot(query_vec) ** 0.5
    dot_product = query_vec.dot(doc_vec)

    denom = query_mod * doc_mod
    if denom == 0:
        return 0

    return dot_product/denom


def search_query(query):
    ''' Preprocesses the query to generate terms, and uses these 
    terms to find the top 10 documents with largest cosine
    similarity. 
    Parameters :
        query - string
    '''

    global vocab_json, json_list

    DATASET_DIRECTORY_NAME = "lyrics-dataset"
    results_json = []

    if not os.path.isdir(os.path.join(os.getcwd(), DATASET_DIRECTORY_NAME)):
        return results_json

    os.chdir(DATASET_DIRECTORY_NAME)

    corpus = os.listdir(os.getcwd())
    corpus_size = len(corpus) - 1

    if vocab_json is None or json_list is None:
        with open("vocab.json", "r") as vocab_file:
            vocab_json = json.load(vocab_file)

        json_list = []
        for file_name in corpus:
            if file_name == "vocab.json":
                continue

            with open(file_name, "r") as song_file:
                song_json = json.load(song_file)
                json_list.append(song_json)

    os.chdir("..")


    terms = preprocessor.generate_terms(query)
    unique_terms = list(set(terms))

    query_vec = np.array([terms.count(term) for term in unique_terms])
    query_vec = np.log(1 + query_vec)

    doc_freq = np.array([vocab_json.get(term, 0) for term in unique_terms])
    inv_doc_freq = np.log(corpus_size/(1+doc_freq))

    query_vec = query_vec * inv_doc_freq


    top_results = []
    for (idx, song_json) in enumerate(json_list):
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
        song_json = json_list[result[1]]
        if sim > 0:
            song_json["sim"] = sim
            results_json.append(song_json)

    return results_json
