#!/usr/bin/env python3
"""
quantum_variational_mux.py — §-LANG v2.3 Quantum Variational Multiplexer
Qiskit 2.4 | H_enc = I - |x><x| | VQE encodes §S nodes as 3-qubit states

Author: Jesús Vilela Jato (§-LANG research, 2026)
"""
from __future__ import annotations
import re, json, math
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Statevector, DensityMatrix, entropy as vn_entropy
from scipy.optimize import minimize

N_QUBITS, DIM, REPS, MUX_K = 3, 8, 3, 4
ADIABAT_STEPS, EPSILON_FIDEL, SAL_THRESHOLD = 30, 0.85, 1.8

@dataclass
class SectionNode:
    label: str; x: np.ndarray; sal: float
    @property
    def norm(self): return float(np.linalg.norm(self.x))
    @property
    def amplitude(self):
        n = self.norm
        return self.x / n if n > 1e-12 else np.ones(DIM) / math.sqrt(DIM)
    def H_enc(self):
        p = self.amplitude.reshape(-1,1)
        return np.eye(DIM) - (p @ p.T.conj())
    def H_mix(self):
        H = np.zeros((DIM,DIM))
        for i in range(N_QUBITS):
            X = np.array([[0,1],[1,0]])
            mats = [X if q==i else np.eye(2) for q in range(N_QUBITS)]
            Xi = mats[0]
            for m in mats[1:]: Xi = np.kron(Xi,m)
            H -= Xi
        return H

@dataclass
class VQEChannel:
    ch_id: int; energy: float; fidelity: float
    theta_star: np.ndarray; sv: np.ndarray; vn_s: float; iters: int

@dataclass
class AQ:
    gap: np.ndarray; gs_fid: np.ndarray; sigma20: bool

@dataclass
class MuxResult:
    node: SectionNode; channels: list; aq: AQ
    best_ch: int; sigma18: bool; sigma19: bool

def build_ansatz():
    n, n_params = N_QUBITS, N_QUBITS*(REPS+1)
    theta = ParameterVector("θ", n_params)
    qc = QuantumCircuit(n); idx = 0
    for _ in range(REPS):
        for q in range(n): qc.ry(theta[idx], q); idx+=1
        for q in range(n): qc.cx(q,(q+1)%n)
    for q in range(n): qc.ry(theta[idx], q); idx+=1
    return qc, theta

def sv_from_theta(qc, vals):
    return Statevector(qc.assign_parameters(vals)).data

def run_vqe(ch_id, t0, qc, target):
    iters=[0]
    def cost(t): iters[0]+=1; psi=sv_from_theta(qc,t); return 1-abs(np.dot(target.conj(),psi))**2
    r = minimize(cost, t0, method="COBYLA", options={"maxiter":600,"rhobeg":0.3,"catol":1e-7})
    psi = sv_from_theta(qc, r.x)
    fid = float(abs(np.dot(target.conj(), psi))**2)
    s = float(vn_entropy(DensityMatrix(psi), base=2))
    return VQEChannel(ch_id, float(r.fun), fid, r.x, psi, s, iters[0])

def adiabatic_analysis(node):
    He, Hm, tgt = node.H_enc(), node.H_mix(), node.amplitude
    sv = np.linspace(0,1,ADIABAT_STEPS+1)
    gaps, fidels = np.zeros(len(sv)), np.zeros(len(sv))
    for i,s in enumerate(sv):
        Hs = (1-s)*Hm + s*He
        ev, evec = np.linalg.eigh(Hs)
        gaps[i] = ev[1]-ev[0]
        fidels[i] = abs(np.dot(tgt.conj(), evec[:,0]))**2
    return AQ(gaps, fidels, bool(np.all(gaps > 1e-9)))

def qvm(node):
    qc,_ = build_ansatz(); tgt = node.amplitude
    rng = np.random.default_rng(int(abs(hash(node.label)))&0xFFFF)
    seeds = rng.uniform(-np.pi, np.pi, (MUX_K, qc.num_parameters))
    channels = []
    for ch_id in range(MUX_K):
        ch = run_vqe(ch_id, seeds[ch_id], qc, tgt)
        channels.append(ch)
        print(f"  ch={ch_id}  infid={ch.energy:.5f}  fid={ch.fidelity:.4f}  "
              f"S={ch.vn_s:.3f}  iters={ch.iters}")
    best = max(range(MUX_K), key=lambda i: channels[i].fidelity)
    aq = adiabatic_analysis(node)
    print(f"  adiabat: gap_min={aq.gap.min():.4f}  gs_fid_end={aq.gs_fid[-1]:.4f}  "
          f"σ20={'✓' if aq.sigma20 else '✗'}")
    s18 = channels[best].fidelity >= EPSILON_FIDEL
    s19 = all(abs(np.linalg.norm(ch.sv)-1.0)<1e-8 for ch in channels)
    return MuxResult(node, channels, aq, best, s18, s19)

SECTION_RE = re.compile(r"^§S\{label=([^,]+), x=\[([^\]]+)\], sal=([0-9.]+)\}$")
def parse_lang(p):
    ns=[]
    for line in p.read_text(encoding="utf-8").splitlines():
        m = SECTION_RE.match(line.strip())
        if m:
            x = np.array([float(v.strip()) for v in m.group(2).split(",")])
            ns.append(SectionNode(m.group(1),x,float(m.group(3))))
    return ns

def report(results):
    rows=[]
    for r in results:
        b=r.channels[r.best_ch]
        v="COMMIT" if r.sigma18 and r.sigma19 and r.aq.sigma20 else "BLOCK"
        rows.append({"label":r.node.label,"norm":round(r.node.norm,5),"sal":r.node.sal,
            "fidelity":round(b.fidelity,5),"infidelity":round(b.energy,5),
            "vn_entropy":round(b.vn_s,4),"gap_min":round(float(r.aq.gap.min()),5),
            "gs_fid_end":round(float(r.aq.gs_fid[-1]),5),
            "sigma18":r.sigma18,"sigma19":r.sigma19,"sigma20":r.aq.sigma20,"verdict":v})
    mf=round(sum(r["fidelity"] for r in rows)/len(rows),5)
    return {"version":"§-LANG v2.3 QVM","n_qubits":N_QUBITS,"mux_k":MUX_K,
            "reps":REPS,"epsilon_fidelity":EPSILON_FIDEL,"n_nodes":len(rows),
            "results":rows,
            "summary":{"verdict":"COMMIT" if all(r["verdict"]=="COMMIT" for r in rows) else "PARTIAL_BLOCK",
                "mean_fidelity":mf,
                "all_sigma18":all(r.sigma18 for r in results),
                "all_sigma19":all(r.sigma19 for r in results),
                "all_sigma20":all(r.aq.sigma20 for r in results)}}

def main():
    import sys
    p = Path(sys.argv[1]) if len(sys.argv)>1 else Path("LANG.v2.3.quantum_autocompressor.lang")
    nodes = parse_lang(p)
    targets = [n for n in nodes if n.norm>1e-4 and n.sal>=SAL_THRESHOLD]
    print(f"§-LANG QVM | {len(nodes)} nodes | {len(targets)} targets (sal≥{SAL_THRESHOLD}) | k={MUX_K}\n")
    results=[]
    for i,node in enumerate(targets):
        print(f"[{i+1}/{len(targets)}] §S:{node.label:<22} ‖x‖={node.norm:.4f}  sal={node.sal}")
        r = qvm(node); results.append(r)
        b=r.channels[r.best_ch]
        v="COMMIT" if r.sigma18 and r.sigma19 and r.aq.sigma20 else "BLOCK"
        print(f"  → fid={b.fidelity:.4f}  σ18={r.sigma18} σ19={r.sigma19} σ20={r.aq.sigma20}  [{v}]\n")
    rep = report(results)
    out=Path("research/qvm_report.json"); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(rep,indent=2),encoding="utf-8")
    s=rep["summary"]
    print("─"*60)
    print(f"Nodes={rep['n_nodes']}  mean_fidelity={s['mean_fidelity']}")
    print(f"σ18={s['all_sigma18']}  σ19={s['all_sigma19']}  σ20={s['all_sigma20']}")
    print(f"VERDICT: {s['verdict']}")

if __name__=="__main__": main()
