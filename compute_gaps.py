import csv
import os
from collections import defaultdict

REFERENCE_CONFIG = "VI2+VI4"

def compute_gaps(input_csv, output_csv, reference_config=REFERENCE_CONFIG):
    by_instance = defaultdict(lambda: {"base": [], "heuristics": []})
    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            inst = row.get("Instance")
            alg = row.get("Algorithm")
            if not inst or not alg:
                continue
            try:
                obj = float(row.get("ObjVal", "nan"))
            except:
                continue
            bound_val = row.get("ObjBound")
            try:
                lb = float(bound_val) if bound_val is not None and bound_val != "" else None
            except:
                lb = None
            if alg == "base":
                by_instance[inst]["base"].append({
                    "ObjVal": obj,
                    "ObjBound": lb,
                    "Config": row.get("Config")
                })
            elif alg in ("lns", "ils"):
                by_instance[inst]["heuristics"].append({
                    "Algorithm": alg,
                    "ObjVal": obj,
                    "Config": row.get("Config")
                })

    rows = []
    for inst, data in by_instance.items():
        base_rows = data["base"]
        if not base_rows:
            continue
        ref_model_row = next((r for r in base_rows if r["Config"] == reference_config), None)
        ref_model_val = ref_model_row["ObjVal"] if ref_model_row else None
        ref_lb = ref_model_row["ObjBound"] if ref_model_row else None
        for hr in data["heuristics"]:
            heur_val = hr["ObjVal"]
            if ref_model_val and ref_model_val != 0:
                gap_model_cfg = (heur_val - ref_model_val) / ref_model_val
            else:
                gap_model_cfg = None
            if ref_lb and ref_lb != 0:
                gap_lb_cfg = (heur_val - ref_lb) / ref_lb
            else:
                gap_lb_cfg = None
            rows.append({
                "Instance": inst,
                "Heuristic": hr["Algorithm"],
                "HeuristicObjVal": heur_val,
                "RefConfig": reference_config,
                "RefModelObjVal": ref_model_val,
                "RefLB": ref_lb,
                "GapToModelRefConfig": gap_model_cfg,
                "GapToLBRefConfig": gap_lb_cfg,
            })

    fieldnames = [
        "Instance",
        "Heuristic",
        "HeuristicObjVal",
        "RefConfig",
        "RefModelObjVal",
        "RefLB",
        "GapToModelRefConfig",
        "GapToLBRefConfig",
    ]
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    input_csv = os.path.join(base_dir, "results", "results.csv")
    output_csv = os.path.join(base_dir, "results", "gaps.csv")
    compute_gaps(input_csv, output_csv)