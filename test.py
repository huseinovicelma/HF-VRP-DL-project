import os
import time
from src.parser import read_instance
from src.model import build_model
from src.heuristics import lns_matheuristic
import csv

vi_combinations = [
    ({}, "base"),
    ({"vi13": True}, "vi13"),
    ({"vi14": True}, "vi14"),
    ({"vi13": True, "vi14": True}, "vi13+vi14"),
]
euristics = ['DIV', 'INT', 'REC']
params = {'ITERMAX': 50, 'MAXNOIMPROVE': 10, 'm_pert': 3}

instances_dir = "dataset/HF-VRP-DL-instances"
results_dict = {}

for filename in sorted(os.listdir(instances_dir)):
    if filename.endswith('.txt'):
        data = read_instance(os.path.join(instances_dir, filename))
        results_dict[filename] = {}
        # Modello esatto con tutte le combinazioni di VI
        for vi_flags, vi_name in vi_combinations:
            m = build_model(data, vi_flags)
            start = time.time()
            m.optimize()
            elapsed = time.time() - start
            results_dict[filename][f"{vi_name}_time"] = round(elapsed, 2)
            results_dict[filename][f"{vi_name}_cost"] = round(m.objVal, 2) if m.status == 2 else ""
        # Euristiche
        for algo_type in euristics:
            start = time.time()
            sol = lns_matheuristic(data, build_model, params, algo_type=algo_type)
            elapsed = time.time() - start
            results_dict[filename][f"LNS-{algo_type}_time"] = round(elapsed, 2)
            results_dict[filename][f"LNS-{algo_type}_cost"] = round(sol['cost'], 2) if sol['cost'] < float('inf') else ""

# Scrivi il file CSV
columns = (
    ["istanza"] +
    sum([[f"{name}_time", f"{name}_cost"] for _, name in vi_combinations], []) +
    sum([[f"LNS-{e}_time", f"LNS-{e}_cost"] for e in euristics], [])
)
with open("results/risultati_test_tabella.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    for filename, res in results_dict.items():
        row = [filename] \
            + sum([[res.get(f"{name}_time", ""), res.get(f"{name}_cost", "")] for _, name in vi_combinations], []) \
            + sum([[res.get(f"LNS-{e}_time", ""), res.get(f"LNS-{e}_cost", "")] for e in euristics], [])
        writer.writerow(row)