```python
def constant_oracle(input_size, num_qubits):

  qc = QuantumCircuit(num_qubits, name="Uf")

  output = np.random.randint(2)

  if output == 1:

   qc.x(input_size)

  global C_ORACLE_

  if C_ORACLE_ is None or num_qubits <= 6:

    if num_qubits < 9:

      C_ORACLE_ = qc

  return qc
```

```python
def balanced_oracle(input_size, num_qubits):

  qc = QuantumCircuit(num_qubits, name="Uf")

  b_str = "".join('1' if i % 2 == 0 else '0' for i in range(input_size))

  for qubit in range(input_size):

    if b_str[qubit] == '1':

      qc.x(qubit)

  qc.barrier()

  for qubit in range(input_size):

    qc.cx(qubit, input_size)

  qc.barrier()

  for qubit in range(input_size):

    if b_str[qubit] == '1':

      qc.x(qubit)

  global B_ORACLE_

  if B_ORACLE_ is None or num_qubits <= 6:

    if num_qubits < 9:

      B_ORACLE_ = qc

  return qc
```

```python
def DeutschJozsa(num_qubits, type):

  input_size = num_qubits - 1

  qr = QuantumRegister(num_qubits)

  cr = ClassicalRegister(input_size)

  qc = QuantumCircuit(qr, cr, name=f"dj-{num_qubits}-{type}")

  for qubit in range(input_size):

    qc.h(qubit)

  qc.x(input_size)

  qc.h(input_size)

  qc.barrier()

  Uf = constant_oracle(input_size, num_qubits) if type == 0 else balanced_oracle(input_size, num_qubits)

  qc.append(Uf, qr)

  qc.barrier()

  for qubit in range(num_qubits):

    qc.h(qubit)

  qc.x(input_size)

  qc.barrier()

  for i in range(input_size):

    qc.measure(i, i)

  global QC_

  if QC_ is None or num_qubits <= 6:

    if num_qubits < 9:

      QC_ = qc

  return qc
```

```python
def analyze_and_print_result(qc, result, num_qubits, type, num_shots):

  input_size = num_qubits - 1

  counts = result.get_counts(qc)

  if verbose:

    print(f"For type {type} measured: {counts}")

  key = '0' * input_size if type == 0 else '1' * input_size

  correct_dist = {key: 1.0}

  fidelity = metrics.polarization_fidelity(counts, correct_dist)

  return counts, fidelity
```

```python
def run(min_qubits=3, max_qubits=8, skip_qubits=1, max_circuits=3, num_shots=100,

    backend_id=None, provider_backend=None,

    hub="ibm-q", group="open", project="main", exec_options=None,

    context=None):

  print(f"{benchmark_name} Benchmark Program - Qiskit")

  max_qubits = max(3, max_qubits)

  min_qubits = min(max(3, min_qubits), max_qubits)

  skip_qubits = max(1, skip_qubits)

  if context is None:

    context = f"{benchmark_name} Benchmark"

  metrics.init_metrics()
```

```python
 def execution_handler(qc, result, num_qubits, type, num_shots):

    num_qubits = int(num_qubits)

    counts, fidelity = analyze_and_print_result(qc, result, num_qubits, int(type), num_shots)

    metrics.store_metric(num_qubits, type, 'fidelity', fidelity)

  ex.init_execution(execution_handler)

  ex.set_execution_target(backend_id, provider_backend=provider_backend,

      hub=hub, group=group, project=project, exec_options=exec_options,

      context=context)

  for num_qubits in range(min_qubits, max_qubits + 1, skip_qubits):

    input_size = num_qubits - 1

    num_circuits = min(2, max_circuits)

    print(f"************\nExecuting [{num_circuits}] circuits with num_qubits = {num_qubits}")

    for type in range(num_circuits):

      ts = time.time()

      qc = DeutschJozsa(num_qubits, type)

      metrics.store_metric(num_qubits, type, 'create_time', time.time() - ts)

      qc2 = qc.decompose()

      ex.submit_circuit(qc2, num_qubits, type, num_shots)

    ex.throttle_execution(metrics.finalize_group)

  ex.finalize_execution(metrics.finalize_group)

  print("Sample Circuit:")

  print(QC_ if QC_ is not None else "  ... too large!")

  print("\nConstant Oracle 'Uf' =")

  print(C_ORACLE_ if C_ORACLE_ is not None else " ... too large or not used!")

  print("\nBalanced Oracle 'Uf' =")

  print(B_ORACLE_ if B_ORACLE_ is not None else " ... too large or not used!")

  metrics.plot_metrics(f"Benchmark Results - {benchmark_name} - Qiskit")
```