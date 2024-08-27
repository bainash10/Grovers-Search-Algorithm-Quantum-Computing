from qiskit import QuantumCircuit, execute
from qiskit.visualization import plot_histogram
from qiskit_aer import Aer

# Define the Grover's search function
def grover_search(oracle, num_qubits):
    # Create a quantum circuit with num_qubits + 1 (for the ancilla qubit)
    qc = QuantumCircuit(num_qubits + 1, num_qubits)
    
    # Apply Hadamard gates to all qubits
    qc.h(range(num_qubits))
    qc.h(num_qubits)  # Apply Hadamard gate to ancilla qubit
    
    # Apply the oracle
    qc.append(oracle, range(num_qubits + 1))
    
    # Apply Grover diffusion operator
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits)
    qc.mct(range(num_qubits), num_qubits)  # Multi-controlled Toffoli gate
    qc.h(num_qubits)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))
    
    # Measure the qubits
    qc.measure(range(num_qubits), range(num_qubits))
    
    return qc

# Define the Oracle for the marked item
def create_oracle(num_qubits, marked_index):
    oracle = QuantumCircuit(num_qubits + 1)
    # Convert the marked index to a binary string
    marked_bin = format(marked_index, f'0{num_qubits}b')
    
    # Apply X gates to flip the bits corresponding to the marked item
    for qubit, bit in enumerate(marked_bin):
        if bit == '0':
            oracle.x(qubit)
    
    # Apply the Z gate to flip the sign of the marked item
    oracle.h(num_qubits)
    oracle.mct(range(num_qubits), num_qubits)  # Multi-controlled Toffoli gate
    oracle.h(num_qubits)
    
    # Apply X gates to revert the changes
    for qubit, bit in enumerate(marked_bin):
        if bit == '0':
            oracle.x(qubit)
    
    return oracle

# Parameters
num_qubits = 2
marked_index = 2  # The index of the marked item (2 in this case, representing binary 10)

# Create the oracle for the marked item
oracle = create_oracle(num_qubits, marked_index)

# Create the Grover search circuit
grover_circuit = grover_search(oracle, num_qubits)

# Use Aer's qasm_simulator to simulate the quantum circuit
simulator = Aer.get_backend('qasm_simulator')

# Execute the circuit
job = execute(grover_circuit, simulator, shots=1024)
result = job.result()

# Get the results from the simulation
counts = result.get_counts(grover_circuit)

# Print the result counts
print("\nResult Counts:")
print(counts)

# Visualize the result counts as a histogram
plot_histogram(counts).show()
