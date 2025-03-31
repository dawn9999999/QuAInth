from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Dict

# Load model and tokenizer
model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Configure prompt strategies
PROMPT_STRATEGIES = {
    "block1": {
        "stage1": {
            "name": "block1_stage1",
            "template": """Generate a ONE-SENTENCE description of the function's purpose.
DO NOT mention parameters or formulas.
STRICTLY follow this format: [One-sentence purpose]

Function signature:
{signature}
""",
            "system_role": "You are a concise code summarizer. Respond in a single sentence."
        },
        "stage2": {
            "name": "block1_stage2",
            "template": """Generate descriptions of the function's purpose. STRICTLY follow this format:
1. Implementation: [Description of operations]
2. Quantum Information: [LaTeX representation of gate operations/formulas]
3. Variables: [List all variables with [name]=[role]]

Code to analyze:
{code}
""",
            "system_role": "You are a quantum engineer. Ensure clarity and strict formatting."
        },
        "stage3": {
            "name": "block1_stage3",
            "template": """Generate a detailed, professional annotation for the following quantum function used in Quantum Fourier Transform Benchmark Program. 
STRICTLY follow this format:
1. Algorithm Role: [Detailed description of this code block in Quantum Fourier Transform Benchmark Program]
2. Quantum Formula/Gates Involved: [LaTeX representation of gate operations/formulas]
3. Algorithm Parameters: [List parameters with [name]=[mathematical meaning]]

Code to analyze:
{code}
""",
            "system_role": "You are a quantum algorithm expert. Provide explicit formulas and parameter meanings."
        }
    },
    "block2": {
        "stage1": {
            "name": "block2_stage1",
            "template": """Generate a ONE-SENTENCE description of the function's purpose for quantum circuits.
DO NOT mention parameters or formulas.
STRICTLY follow this format: [One-sentence purpose]

Function signature:
{signature}
""",
            "system_role": "You are a concise code summarizer. Respond in a single sentence."
        },
        "stage2": {
            "name": "block2_stage2",
            "template": """Generate descriptions of the function's purpose. STRICTLY follow this format:
1. Implementation: [Description of operations]
2. Quantum Information: [LaTeX representation of gate operations/formulas]
3. Variables: [List all variables with [name]=[role]]

Code to analyze:
{code}
""",
            "system_role": "You are a quantum engineer. Ensure clarity and strict formatting."
        },
        "stage3": {
            "name": "block2_stage3",
            "template": """Generate a detailed, professional annotation for the following quantum function used in Quantum Fourier Transform Benchmark Program. 
STRICTLY follow this format:
1. Algorithm Role: [Detailed description of this code block in Quantum Fourier Transform Benchmark Program]
2. Quantum Formula/Gates Involved: [LaTeX representation of gate operations/formulas]
3. Algorithm Parameters: [List parameters with [name]=[mathematical meaning]]

Code to analyze:
{code}
""",
            "system_role": "You are a quantum algorithm expert. Provide explicit formulas and parameter meanings."
        }
    },
    "block3": {
        "stage1": {
            "name": "block1_stage1",
            "template": """Generate a ONE-SENTENCE description of the function's purpose.
DO NOT mention parameters or formulas.
STRICTLY follow this format: [One-sentence purpose]

Function signature:
{signature}
""",
            "system_role": "You are a concise code summarizer. Respond in a single sentence."
        },
        "stage2": {
            "name": "block1_stage2",
            "template": """Generate descriptions of the function's purpose. STRICTLY follow this format:
1. Implementation: [Description of operations]
2. Quantum Information: [LaTeX representation of gate operations/formulas]
3. Variables: [List all variables with [name]=[role]]

Code to analyze:
{code}
""",
            "system_role": "You are a quantum engineer. Ensure clarity and strict formatting."
        },
        "stage3": {
            "name": "block1_stage3",
            "template": """Generate a detailed, professional annotation for the following quantum function used in Quantum Fourier Transform Benchmark Program. 
STRICTLY follow this format:
1. Algorithm Role: [Detailed description of this code block in Quantum Fourier Transform Benchmark Program]
2. Quantum Formula/Gates Involved: [LaTeX representation of gate operations/formulas]
3. Algorithm Parameters: [List parameters with [name]=[mathematical meaning]]

Code to analyze:
{code}
""",
            "system_role": "You are a quantum algorithm expert. Provide explicit formulas and parameter meanings."
        }
    }
}

def read_code_blocks(file_path: str) -> List[Dict[str, str]]:
    """Read and preprocess code blocks from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    blocks = content.split("\ndef ")  # Split by function definition
    results = []
    for i, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue
        if not block.startswith("def "):
            block = "def " + block
        lines = block.split("\n")
        signature = lines[0].strip()
        code = "\n".join(lines)
        results.append({"name": f"block_{i + 1}", "signature": signature, "code": code})
    return results

def detect_block_type(signature: str) -> str:
    """Detect block type based on function signature."""
    if "qedc_benchmarks_init" in signature.lower():
        return "block1"
    elif "run" in signature.lower():
        return "block2"
    elif "execution_handler" in signature.lower():
        return "block3"
    return "unknown"

def generate_comments(signature: str, code: str, block_type: str) -> Dict[str, str]:
    """Generate comments using stage-specific strategies."""
    results = {}
    if block_type not in PROMPT_STRATEGIES:
        return {"error": f"Unknown block type: {block_type}"}
    strategies = PROMPT_STRATEGIES[block_type]
    for stage, strategy in strategies.items():
        content = strategy["template"].format(signature=signature, code=code)
        messages = [
            {"role": "system", "content": strategy["system_role"]},
            {"role": "user", "content": content}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(
            generated_ids[0][len(model_inputs.input_ids[0]):], 
            skip_special_tokens=True
        ).strip()
        results[stage] = response
    return results

def save_comparison_results(all_results: List[Dict], output_file: str):
    """Save generated comments with clear formatting."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for idx, block_results in enumerate(all_results, 1):
            f.write(f"【Code Block {idx}】\n")
            for stage_name, comment in block_results.items():
                f.write(f"=== {stage_name.replace('_', ' ').title()} ===\n")
                f.write(f"{comment}\n\n")
            f.write("■" * 50 + "\n\n")

def main(input_file: str, output_file: str):
    """Main execution flow."""
    code_blocks = read_code_blocks(input_file)
    all_results = []
    print(f"Processing {len(code_blocks)} code blocks...")
    for i, block in enumerate(code_blocks, 1):
        block_type = detect_block_type(block["signature"])
        print(f"  Processing block {i}/{len(code_blocks)} ({block_type})")
        comments = generate_comments(block["signature"], block["code"], block_type)
        all_results.append(comments)
    save_comparison_results(all_results, output_file)
    print(f"Generated comments saved to: {output_file}")

if __name__ == "__main__":
    input_file = "C:/Users/PC/Desktop/qrs/code/dsc/code_blocks_qft.txt"  # Input file with code snippets
    output_file = "C:/Users/PC/Desktop/qrs/code/dsc/generated_comments_qft.txt"  # Output file for results
    main(input_file, output_file)
