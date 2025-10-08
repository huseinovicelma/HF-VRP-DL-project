import numpy as np
import math
from src.parse import parse_instance

configs = {
    "No VI"        : (False, False, False, False),
    "VI1"          : (True,  False, False, False),
    "VI2"          : (False, True,  False, False),
    "VI3"          : (False, False, True,  False),
    "VI4"          : (False, False, False, True),
    "VI1+VI4"      : (True,  False, False, True),
    "VI2+VI4"      : (False, True,  False, True),
    "VI3+VI4"      : (False, False, True,  True),
    "All VI"       : (True,  True,  True,  True),
}

def compute_distances(coords, speed=2.0):
    n = len(coords)
    t = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            euclidean = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
            t[i][j] = euclidean / speed
    return t


def extract_model_stats(model):
    return {
        "ObjVal": model.objVal,
        "ObjBound": model.ObjBound,
        "MIPGap": model.MIPGap,
        "RuntimeGurobi": model.Runtime,
        "Status": model.status
    }

def get_parameters(instance_path):
    I, I0, S, Q, q, L, coord, c, r = parse_instance(instance_path)
    t = compute_distances(coord, speed=2.5)
    return I, I0, S, Q, q, L, t, c, r

def print_stats(stats, title=None):
    if title:
        print(f"\n {title}")
    else:
        print("\n Statistiche di ottimizzazione")
    print("-" * 40)
    for k, v in stats.items():
        if isinstance(v, float):
            print(f"{k:<15}: {v:.4f}")
        else:
            print(f"{k:<15}: {v}")
    print("-" * 40)

def save_stats(stats, writer, instance_name, algorithm, config_name):
    stats_row = stats.copy()
    stats_row["Instance"] = instance_name
    stats_row["Algorithm"] = algorithm
    stats_row["Config"] = config_name
    writer.writerow(stats_row)


