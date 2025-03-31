#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import string
from difflib import SequenceMatcher

texts = [
    """### Implementation
The `BersteinVazirani` function implements the Bernstein-Vazirani algorithm to perform quantum computation on a given number of qubits. It uses a quantum circuit to simulate the algorithm, including creating an oracle and applying it to the input bits.

### Quantum Formula
The algorithm uses the following quantum gates:
- X gate: To flip the state of a qubit.
- H gate: To create a superposition of the qubit.
- CNOT gate: To perform a controlled NOT gate.
- Measure gate: To measure the state of a qubit.

### Parameters
- num_qubits: The number of qubits in the system.
- secret_int: The integer to be encrypted.
- hidden_bits: A list of integers representing the positions of hidden bits.
- method: The method used to perform the computation (1 for Oracle-based, 2 for classical-based).
""",
    """This code implements the Bernstein-Vazirani algorithm in Python. The algorithm is designed to find a state that is close to a target state based on a given number of qubits, a secret integer, and a list of hidden bits. The algorithm can be implemented using the Qiskit library in Python. The code includes a function `BersteinVazirani` that takes in the number of qubits, the secret integer, the list of hidden bits, and an optional method parameter. The function uses the Qiskit library to decompose the quantum circuit into simpler components and then applies the appropriate oracle function based on the method parameter. The function returns the decomposed circuit.
""",
    """The function `BersteinVazirani` performs a quantum circuit operation using a given number of qubits, a secret integer, and a list of hidden bits. It applies a series of operations based on the specified method (1 or 2). The function uses a quantum register and classical registers to represent the quantum circuit."""
]


def extract_keywords(text, top_n=5):

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    

    filtered_words = [w for w in words if w.isalpha() and w not in stop_words]
    

    freq_dict = {}
    for w in filtered_words:
        freq_dict[w] = freq_dict.get(w, 0) + 1
    

    sorted_words = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    
    return [w[0] for w in sorted_words[:top_n]]



def split_into_sentences(text):

    return sent_tokenize(text)


def sentence_similarity(s1, s2, threshold=0.85):

    return SequenceMatcher(None, s1, s2).ratio()


def merge_and_deduplicate(sentences_list, sim_threshold=0.85):

    merged_sentences = []
    
    for sent in sentences_list:

        duplicated = False
        for ms in merged_sentences:
            sim = sentence_similarity(sent, ms, threshold=sim_threshold)
            if sim > sim_threshold:
                duplicated = True
                break
        if not duplicated:
            merged_sentences.append(sent)
    
    return merged_sentences



def process_texts(texts):

    

    for i, t in enumerate(texts):
        kw = extract_keywords(t)
        print(kw)
        print('-' * 60)
    
    all_sentences = []
    for t in texts:
        sents = split_into_sentences(t)
        all_sentences.extend(sents)
    
    dedup_sentences = merge_and_deduplicate(all_sentences)
    
    return dedup_sentences


if __name__ == "__main__":

    merged_result = process_texts(texts)
    

    for idx, s in enumerate(merged_result, 1):
        print(f"{idx}. {s}")
    

    final_text = " ".join(merged_result)
    print(final_text)
