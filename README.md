# QuAInth

## Description

This repository incorporates the artifact involved in the manuscript '*QuAInth: A Code Annotation Approach for Application-oriented Quantum Programs via N-version LLMs*'.  

More details will be updated if the manuscript is possibly accepted for publication.

## Environment

First create a conda environment, such as named QuAInth.

```
conda create -n QuAInth python=3.11.7
```

Then, activate the environment and install the packages in `requirement.txt`.

```
conda activate QuAInth
pip install -r requirement.txt
```

Here are the requirements:

```
transformers >=4.49.0
torch >=2.5.1
qiskit >= 0.45.1
nltk >= 3.9.1
scikit-learn >= 1.5.2
rouge_score >= 0.1.2
```

## Code

This repository contains 3 folders, which are "`aqps`", "`evaluate`" and "`llms`".
### Object Programs
Object Programs are shown in `aqps`.
- `aaa.py`: AQPs downloaded from `QC-App-Oriented-Benchmarks` ([link]([https://github.com/Qiskit/qiskit/tree/stable/1.2/qiskit/circuit/library](https://github.com/SRI-International/QC-App-Oriented-Benchmarks/tree/master?tab=readme-ov-file))), where `aaa` refers to the name of the object program (i.e., `bv_kenel`, `dj_benchmark`, `grovers_kenel` and `qft_benchmark`).

- `code_blocks_aaa.md`: Code blocks of AQPs segmented based on function signatures.

### Implementation

Main steps of annotation generation via LLMs are shown in `llms`.

- `bbb.py`: Run `bbb.py` to generate annotations, where `bbb` refers to the names of llms (i.e., qwen, deepseeker and llama). Before execution, make sure the required models have been downloaded via `Hugging Face Transformers`. Specifically, **Qwen2.5-Coder-0.5B-Instruct** and **deepseek-coder-1.3b-instruct** can be downloaded directly, while **Llama-3.2-1B-Instruct** requires usage approval and verification via a `Hugging Face token`. Ensure that the GPU has sufficient memory, as the runtime depends on the GPU's capacity.  

Modify the prompt in `PROMPT_STRATEGIES` to provide appropriate contextual information for specific AQPs. In the `generate_comments` function, you can adjust parameters such as `max_new_tokens` and `temperature` to control the maximum generation length and the model's randomness.

The generated annotations will be saved in a .txt file with the following format:
```
【Code Block 1】

=== Stage1 ===

<Annotation generated using Stage 1 prompt>

=== Stage2 ===

<Annotation generated using Stage 2 prompt>

=== Stage3 ===

<Annotation generated using Stage 3 prompt>

■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

【Code Block 2】
```

### Data Processing

Scoring codes are shown in `evaluate`.

- `rogue.py`, `cos.py`, `judge.py` and `total_score.py`: Compute _RF1_, _CS_, _QS_ and _FS_ for generated annotations.

- `combine.py`: This script uses `NumPy` and `scikit-learn` to perform weighted text fusion based on their importance scores.
