import stim

from qiskit import QuantumCircuit
from qiskit.circuit import Gate


def make_circlevel_by_replacement(stim_qc, gate):
    """
    Converts a stim.Circuit object into a qiskit QuantumCircuit, replacing error instructions with the provided gate. 
    This gate represents the entry point for Matcha noisy simulator, which has to be configured on the emulator level.
    "DETECTOR" and "OBSERVABLE_INCLUDE" instructions are converted into gates where the classical parameters refer to the measure offset that is going to be XORed to compose the detector bits.
    """
    assert isinstance(stim_qc, stim.Circuit), "Input must be a stim.Circuit object"

    qc = QuantumCircuit(stim_qc.num_qubits)

    __qiskit_methods = {
        "CX": qc.cx,
        "H": qc.h,
        "X": qc.x,
        "Y": qc.y,
        "Z": qc.z,
        "I": qc.id,
    }

    first_tick = True

    for op in stim_qc:

        if op.name in ["QUBIT_COORDS", "SHIFT_COORDS"]:
            continue

        elif op.name == "TICK":
            first_tick = False
            qc.barrier()

        elif op.name in __qiskit_methods:
            sites = [[t.value for t in tg] for tg in op.target_groups()]
            for sg in sites:
                __qiskit_methods[op.name](*sg)

        elif op.name in ["X_ERROR", "Y_ERROR", "Z_ERROR", "DEPOLARIZE1", "DEPOLARIZE2"]:

            sites = [[t.value for t in tg] for tg in op.target_groups()]
            for sg in sites:
                for ss in sg:
                    qc.append(gate.to_gate(), [ss])

        elif op.name in ["M", "MZ", "R", "RZ", "MR", "MRZ", "MX", "RX", "MRX"]:

            sites = [[t.value for t in tg] for tg in op.target_groups()]

            if first_tick:
                if op.name in ["R", "RZ", "RX"]:  # all the options without M ...
                    if op.name == "RX":
                        for sg in sites:
                            qc.h(sg)
                    else:
                        # assuming initial state is |0000...>
                        pass

                continue

            for sg in sites:
                qc.barrier()
                qc.append(Gate(name=op.name, num_qubits=1, params=[]), sg)

        elif op.name in ["DETECTOR", "OBSERVABLE_INCLUDE"]:
            sites = [tar.value for tar in op.targets_copy()]

            qc.barrier()
            this_det = Gate(name=op.name, num_qubits=1, params=sites)
            qc.append(this_det, [0])

        else:
            raise ValueError(f"UNKNOWN OP: {op}")

    qc.barrier()
    return qc
