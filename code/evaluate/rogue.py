from rouge_score import rouge_scorer

# Define the reference and candidate texts
reference_text = "This function creates the quantum oracle U_f for the Bernstein-Vazirani algorithm. The oracle encodes the hidden bit string into the quantum state using controlled-X (CX) gates. For each qubit in the `hidden_bits` list (which represents the secret), a CX gate is applied to flip the auxiliary qubit (the last qubit in the register) conditioned on the corresponding hidden bit being 1."
candidate_text_1 = "The function `create_oracle` generates a random Oracle circuit with the specified number of qubits, input size, and hidden bits."
candidate_text_2 = "Initialize the quantum circuit with a single qubit, Create the oracle logic, Measure the output"
candidate_text_3 = "The function `create_oracle` is designed to create a quantum oracle that can be used to simulate the behavior of a quantum system under certain conditions."

# Initialize the ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

# Calculate ROUGE-L for each candidate
scores_1 = scorer.score(reference_text, candidate_text_1)
scores_2 = scorer.score(reference_text, candidate_text_2)
scores_3 = scorer.score(reference_text, candidate_text_3)

# Print the ROUGE-L score for each candidate
print(f"ROUGE-L for Candidate 1: {scores_1['rougeL'].fmeasure:.4f}")
print(f"ROUGE-L for Candidate 2: {scores_2['rougeL'].fmeasure:.4f}")
print(f"ROUGE-L for Candidate 3: {scores_3['rougeL'].fmeasure:.4f}")
