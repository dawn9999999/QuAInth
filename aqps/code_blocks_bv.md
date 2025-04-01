```python
def create_oracle(num_qubits: int, input_size: int, hidden_bits: List[int]):
    qr = QuantumRegister(num_qubits)
    qc = QuantumCircuit(qr, name="Uf")
    for i_qubit in range(input_size):
        if hidden_bits[i_qubit] == 1:
            qc.cx(qr[i_qubit], qr[input_size])
    return qc
```

```python
def BersteinVazirani(num_qubits: int, secret_int: int, hidden_bits: List[int], method: int = 1):
    input_size = num_qubits - 1
    if method == 1:
        qr = QuantumRegister(num_qubits)
        cr = ClassicalRegister(input_size)
        qc = QuantumCircuit(qr, cr, name=f"bv({method})-{num_qubits}-{secret_int}")
        qc.x(qr[input_size])
        for i_qubit in range(num_qubits):
            qc.h(qr[i_qubit])
        qc.barrier()
        Uf = create_oracle(num_qubits, input_size, hidden_bits)
        qc.append(Uf, qr)
        qc.barrier()
        for i_qubit in range(num_qubits):
            qc.h(qr[i_qubit])
        qc.x(qr[input_size])
        qc.barrier()
        for i in range(input_size):
            qc.measure(i, i)
    elif method == 2:
        qr = QuantumRegister(2)
        cr = ClassicalRegister(input_size)
        qc = QuantumCircuit(qr, cr, name=f"bv({method})-{num_qubits}-{secret_int}")
        qc.x(qr[1])
        qc.h(qr[1])
        qc.barrier()
        Uf = None
        for i_qubit in range(input_size):
            if hidden_bits[i_qubit] == 1:
                qc.h(qr[0])
                qc.cx(qr[0], qr[1])
                qc.h(qr[0])
            qc.measure(qr[0], cr[i_qubit])
            qc.reset([0] * num_resets)
    global QC_, Uf_
    if QC_ == None or num_qubits <= 6:
        if num_qubits < 9: QC_ = qc
    if Uf_ == None or num_qubits <= 6:
        if num_qubits < 9: Uf_ = Uf
    qc2 = qc.decompose()
    return qc2
```

```python
def kernel_draw():
    print("Sample Circuit:")
    print(QC_ if QC_ != None else "  ... too large!")
    if Uf_ != None:
        print("\nQuantum Oracle 'Uf' =")
        print(Uf_ if Uf_ != None else " ... too large!")
```

