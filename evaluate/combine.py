import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(texts):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

def weighted_fusion(texts, weights):
    similarity_matrix = calculate_cosine_similarity(texts)
    
    weighted_text = []
    
    for i, text in enumerate(texts):
        weighted_sentence = []
        for j, word in enumerate(text.split()):
            word_weights = np.dot(similarity_matrix[i], weights)
            weighted_sentence.append((word, word_weights))
        
        weighted_sentence.sort(key=lambda x: x[1], reverse=True)
        weighted_text.append(' '.join([word for word, _ in weighted_sentence]))
    
    return ' '.join(weighted_text)
total_scores = [0.32, 0.47, 0.61]

sum_scores = sum(total_scores)

weights = [score / sum_scores for score in total_scores]

texts = [
    "The function `BersteinVazirani` performs a quantum circuit operation using a given number of qubits, a secret integer, and a list of hidden bits. It applies a series of operations based on the specified method (1 or 2). The function uses a quantum register and classical registers to represent the quantum circuit.",
    "This code implements the Bernstein-Vazirani algorithm in Python. The algorithm is designed to find a state that is close to a target state based on a given number of qubits, a secret integer, and a list of hidden bits. The algorithm can be implemented using the Qiskit library in Python. The code includes a function `BersteinVazirani` that takes in the number of qubits, the secret integer, the list of hidden bits, and an optional method parameter. The function uses the Qiskit library to decompose the quantum circuit into simpler components and then applies the appropriate oracle function based on the method parameter. The function returns the decomposed circuit.",
    "The `BersteinVazirani` function implements the Bernstein-Vazirani algorithm to perform quantum computation on a given number of qubits. It uses a quantum circuit to simulate the algorithm, including creating an oracle and applying it to the input bits."
]

weighted_text = []
for i, text in enumerate(texts):
    weighted_sentence = f"({weights[i]:.2f}) {text}"
    weighted_text.append(weighted_sentence)

print("Weighted Fused Texts:")
for sentence in weighted_text:
    print(sentence)


fused_text = weighted_fusion(texts, weights)
print("Fused Text:")
print(fused_text)
