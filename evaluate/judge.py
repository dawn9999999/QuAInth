import re
from typing import Dict, List
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer


TRUTH_DB = {
    "create_oracle": {
        "keywords": ["oracle", "Bernstein-Vazirani"],
        "math_patterns": [
            r"U_f=\\bigotimes_{i:s_i=1}\\text{CNOT}_{i,a}",
            r"\|x\\rangle\|y\\oplus f(x)\\rangle",
            r"\|x\\rangle\|y\\otimes f(x)\\rangle"
        ],
        "params": {
            "num_qubits": "Number of qubits",
            "input_size": "Size of the input data",
            "hidden_bits": "Contain values 0 or 1"
        },
        "reference": [
            "Implements Bernstein-Vazirani oracle with CNOT gates",
            "$U_f=\\bigotimes_{i:s_i=1}\\text{CNOT}_{i,a}$",
            "num_qubits=number of qubits, input_size=size of the input data, hidden_bits=contain values 0 or 1"
        ]
    },
    "BersteinVazirani": {
        "keywords": ["Hadamard", "amplitude amplification", "ancilla", "ψ_3", "n+1 qubits"],
        "math_patterns": [
            r"\\|\\psi_3\\rangle=\\|s\\rangle\\|-\\rangle",
            r"\\frac{1}{\\sqrt{2^{n+1}}}\\sum_{x=0}^{2^n-1}\\|x\\rangle",
            r"\\(-1\\)^\\{s\\cdot x\\}"
        ],
        "params": {
            "num_qubits": "n data + 1 ancilla qubits",
            "secret_int": "Integer representation of s"
        },
        "reference": [
            "Implements Bernstein-Vazirani algorithm steps",
            "$\\|\\psi_3\\rangle=\\|s\\rangle\\|-\\rangle$",
            "num_qubits=n+1, secret_int=secret integer s"
        ]
    },
    "kernel_draw": {
        "keywords": ["circuit visualization", "Uf display", "mid-circuit measurement", "virtual qubits"],
        "math_patterns": [
            r"\\|0\\rangle\\^{\\otimes n}\\|1\\rangle",
            r"H\\^{\\otimes n}"
        ],
        "params": {
            "QC_": "QuantumCircuit object",
            "Uf_": "Oracle unitary operator"
        },
        "reference": [
            "Visualizes quantum circuit with oracle",
            "N/A",
            "QC_=Circuit instance, Uf_=Oracle instance"
        ]
    }
}



def parse_generated_comments(file_path: str) -> Dict[str, Dict[str, str]]:
    """Parse the generated comments from a file."""
    comments = {}
    current_block = None
    current_stage = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("【Code Block"):
                current_block = line.strip()
                comments[current_block] = {}
            elif line.startswith("==="):
                stage_name = re.search(r"=== (.*) ===", line).group(1)
                current_stage = stage_name.strip().replace(" ", "_").lower()
                comments[current_block][current_stage] = []
            elif "■■■" in line:
                current_block = None
                current_stage = None
            elif current_block and current_stage:
                comments[current_block][current_stage].append(line.strip())

    structured_comments = {
        block: {stage: "\n".join(content) for stage, content in stages.items()}
        for block, stages in comments.items()
    }
    return structured_comments


def detect_function(comment: str) -> str:
    """Detect the function type based on the comment content."""
    comment_preview = comment[:200].lower()
    if "oracle" in comment_preview:
        return "create_oracle"
    elif "berstein" in comment_preview or "b_v" in comment_preview:
        return "BersteinVazirani"
    elif "circuit" in comment_preview and "draw" in comment_preview:
        return "kernel_draw"
    return "unknown"


def calculate_bleu_rouge(candidate: List[str], reference: List[str]) -> Dict[str, float]:
    """Calculate BLEU and ROUGE scores."""
    if not reference or not candidate:
        return {"bleu": 0.0, "rouge": 0.0}

    bleu_score = sentence_bleu([reference], candidate, weights=(0.25, 0.25, 0.25, 0.25))

    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rouge_result = scorer.score('\n'.join(reference), '\n'.join(candidate))
    rouge_score = rouge_result['rougeL'].fmeasure

    return {"bleu": bleu_score, "rouge": rouge_score}


def evaluate_stage(comment: str, func_name: str) -> Dict[str, float]:
    """Evaluate a single stage of comments."""
    truth = TRUTH_DB.get(func_name, {})
    keywords = [re.escape(kw) for kw in truth.get("keywords", [])]
    keyword_pattern = r"\b(" + "|".join(keywords) + r")\b"
    found_keywords = len(re.findall(keyword_pattern, comment, re.IGNORECASE))
    keyword_score = min(found_keywords / len(keywords), 1.0) if keywords else 0.0

    math_patterns = truth.get("math_patterns", [])
    math_score = sum(1 for pattern in math_patterns if re.search(pattern, comment))
    math_score = min(math_score / len(math_patterns) if math_patterns else 1.0, 1.0)

    params = truth.get("params", {})
    param_score = sum(
        1 for param, desc in params.items() if re.search(rf"\b{re.escape(param)}\b.*?{desc}", comment, re.DOTALL)
    )
    param_score = min(param_score / len(params) if params else 1.0, 1.0)

    reference = truth.get("reference", [])
    candidate = comment.split("\n")
    nl_metrics = calculate_bleu_rouge(candidate, reference)

    return {
        **nl_metrics,
        "keyword_coverage": keyword_score,
        "math_matching": math_score,
        "param_accuracy": param_score,
        "composite_score": (keyword_score * 0.4 + math_score * 0.3 + param_score * 0.3),
    }


def generate_report(evaluation_results: Dict) -> str:
    """Generate a report from evaluation results."""
    report = []
    for block, stages in evaluation_results.items():
        report.append(f"\n{block} Evaluation Results:")
        for stage, scores in stages.items():
            report.append(
                f"  Stage: {stage.replace('_', ' ').title()}\n"
                f"  1. BLEU Score: {scores['bleu']:.4f}\n"
                f"  2. ROUGE-L F1: {scores['rouge']:.4f}\n"
                f"  • Keyword Coverage: {scores['keyword_coverage']:.1%}\n"
                f"  • Math Matching: {scores['math_matching']:.1%}\n"
                f"  • Param Accuracy: {scores['param_accuracy']:.1%}\n"
                f"  • Composite Score: {scores['composite_score']:.1%}\n"
            )
        report.append("━" * 60)
    return "\n".join(report)


def main(input_file: str):
    """Main evaluation workflow."""
    all_comments = parse_generated_comments(input_file)
    evaluation_results = {
        block: {
            stage: evaluate_stage(comment, detect_function(comment))
            for stage, comment in stages.items()
        }
        for block, stages in all_comments.items()
    }
    print(generate_report(evaluation_results))


if __name__ == "__main__":
    input_file = "C:/Users/PC/Desktop/qrs/code/lv1/generated_comments.txt"
    main(input_file)
