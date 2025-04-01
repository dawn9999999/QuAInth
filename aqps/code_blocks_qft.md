```python
def qedc_benchmarks_init(api: str = "qiskit"):

  if api == None: api = "qiskit"

  current_dir = os.path.dirname(os.path.abspath(__file__))

  down_dir = os.path.abspath(os.path.join(current_dir, f"{api}"))

  sys.path = [down_dir] + [p for p in sys.path if p != down_dir]

  up_dir = os.path.abspath(os.path.join(current_dir, ".."))

  common_dir = os.path.abspath(os.path.join(up_dir, "_common"))

  sys.path = [common_dir] + [p for p in sys.path if p != common_dir]

  

  api_dir = os.path.abspath(os.path.join(common_dir, f"{api}"))

  sys.path = [api_dir] + [p for p in sys.path if p != api_dir]

  import execute as ex

  globals()["ex"] = ex

  import metrics as metrics

  globals()["metrics"] = metrics

  from qft_kernel import QuantumFourierTransform, kernel_draw

  return QuantumFourierTransform, kernel_draw


```

```python
def run(min_qubits=2, max_qubits=8, skip_qubits=1, max_circuits=3, num_shots=100,
        method=1, input_value=None,
        backend_id=None, provider_backend=None,
        hub="ibm-q", group="open", project="main", exec_options=None,
        context=None, api=None):
    

QuantumFourierTransform, kernel_draw = qedc_benchmarks_init(api)

print(f"{benchmark_name} ({method}) Benchmark Program - Qiskit")

max_qubits = max(2, max_qubits)
min_qubits = min(max(2, min_qubits), max_qubits)
skip_qubits = max(1, skip_qubits)

if context is None:
    context = f"{benchmark_name} ({method}) Benchmark"

metrics.init_metrics()
```

```python
def execution_handler(qc, result, input_size, s_int, num_shots):
    num_qubits = int(input_size)
    counts, fidelity = analyze_and_print_result(qc, result, num_qubits, int(s_int), num_shots, method)
    metrics.store_metric(input_size, s_int, 'fidelity', fidelity)

ex.init_execution(execution_handler)
ex.set_execution_target(backend_id, provider_backend=provider_backend,
                        hub=hub, group=group, project=project, exec_options=exec_options,
                        context=context)

for input_size in range(min_qubits, max_qubits + 1, skip_qubits):
    np.random.seed(0)
    num_qubits = input_size
    

if method == 1 or method == 2:
    num_circuits = min(2 ** (input_size), max_circuits)
    if 2**(input_size) <= max_circuits:
        s_range = list(range(num_circuits))
    else:
        s_range = np.random.randint(0, 2**(input_size), num_circuits + 2)
        s_range = list(set(s_range))[0:num_circuits]
elif method == 3:
    num_circuits = min(input_size, max_circuits)
    if input_size <= max_circuits:
        s_range = list(range(num_circuits))
    else:
        s_range = np.random.randint(0, 2**(input_size), num_circuits + 2)
        s_range = list(set(s_range))[0:num_circuits]
else:
    sys.exit("Invalid QFT method")

print(f"************\nExecuting [{num_circuits}] circuits with num_qubits = {num_qubits}")

if 2**(input_size) <= max_circuits:
    s_range = list(range(num_circuits))
else:
    s_range = np.random.randint(1, 2**(input_size), num_circuits + 2)
    s_range = list(set(s_range))[0:max_circuits]

for s_int in s_range:
    s_int = int(s_int)
    if input_value is not None:
        s_int = input_value
    

    bitset = str_to_ivec(input_size, s_int)
    if verbose:
        print(f"... s_int={s_int} bitset={bitset}")
    
    ts = time.time()
    qc = QuantumFourierTransform(num_qubits, s_int, bitset, method)
    metrics.store_metric(input_size, s_int, 'create_time', time.time()-ts)
    
    ex.submit_circuit(qc, input_size, s_int, shots=num_shots)

ex.throttle_execution(metrics.finalize_group)  

ex.finalize_execution(metrics.finalize_group)

kernel_draw()

metrics.plot_metrics(f"Benchmark Results - {benchmark_name} ({method}) - Qiskit")
```

