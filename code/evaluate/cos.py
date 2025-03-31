from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


reference_text = "This function creates the quantum oracle U_f for the Bernstein-Vazirani algorithm. The oracle encodes the hidden bit string into the quantum state using controlled-X (CX) gates."
candidate_text_1 = "The function `create_oracle` generates a random Oracle circuit with the specified number of qubits, input size, and hidden bits."
candidate_text_2 = "Initialize the quantum circuit with a single qubit, Create the oracle logic, Measure the output"
candidate_text_3 = "The function `create_oracle` is designed to create a quantum oracle that can be used to simulate the behavior of a quantum system under certain conditions."

vectorizer = TfidfVectorizer(stop_words='english')


tfidf_matrix_1 = vectorizer.fit_transform([reference_text, candidate_text_1])
tfidf_matrix_2 = vectorizer.fit_transform([reference_text, candidate_text_2])
tfidf_matrix_3 = vectorizer.fit_transform([reference_text, candidate_text_3])


cosine_sim_1 = cosine_similarity(tfidf_matrix_1[0], tfidf_matrix_1[1])
cosine_sim_2 = cosine_similarity(tfidf_matrix_2[0], tfidf_matrix_2[1])
cosine_sim_3 = cosine_similarity(tfidf_matrix_3[0], tfidf_matrix_3[1])

print("Cosine Similarity1: ", cosine_sim_1[0][0])
print("Cosine Similarity2: ", cosine_sim_2[0][0])
print("Cosine Similarity3: ", cosine_sim_3[0][0])
